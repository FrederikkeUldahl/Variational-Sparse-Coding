from glob import glob
from pathlib import Path

import pandas as pd
import torch
from torchvision.utils import save_image
from tqdm import tqdm

############################
#from ..logger import Logger
# Manually importing Logger class from logger.py
class Logger(object):
    
    def __init__(self, log_dir ):
        """Create a summary writer logging to log_dir."""
        
        self.train_writer = tf.summary.FileWriter(log_dir + "/train")
        self.test_writer = tf.summary.FileWriter(log_dir + "/eval")

        self.loss = tf.Variable(0.0)
        tf.summary.scalar("loss", self.loss)

        self.merged = tf.summary.merge_all()

        self.session = tf.InteractiveSession()
        self.session.run(tf.global_variables_initializer())


    def scalar_summary(self, train_loss, test_loss, step):
        """Log a scalar variable."""

        summary = self.session.run(self.merged, {self.loss: train_loss})
        self.train_writer.add_summary(summary, step) 
        self.train_writer.flush()

        summary = self.session.run(self.merged, {self.loss: test_loss})
        self.test_writer.add_summary(summary, step) 
        self.test_writer.flush()
###########
class VariationalBaseModel():
    def __init__(self, dataset, width, height, channels, latent_sz, 
                 learning_rate, device, log_interval, normalize=False, 
                 flatten=True):
        self.dataset = dataset
        self.width = width
        self.height = height
        self.channels = channels
        # before width * height * channels
        self.input_sz = (channels, width, height)
        self.latent_sz = latent_sz
        
        self.lr = learning_rate
        self.device = device
        self.log_interval = log_interval
        self.normalize_data = normalize
        self.flatten_data = flatten
        
        # To be implemented by subclasses
        self.model = None
        self.optimizer = None        
    
    
    def loss_function(self):
        raise NotImplementedError
    
    
    def step(self, data, train=False):
        if train:
            self.optimizer.zero_grad()
        output = self.model(data)
        loss = self.loss_function(data, *output, train=train)
        if train:
            loss.backward()
            self.optimizer.step()
        return loss.item()
    
    # TODO: Perform transformations inside DataLoader (extend datasets.MNIST)
    def transform(self, batch):
        if self.flatten_data: 
            batch_size = len(batch)
            batch = batch.view(batch_size, -1)
        if self.normalize_data:
            batch = batch / self.scaling_factor
#         batch_norm = flattened_batch.norm(dim=1, p=2)
#         flattened_batch /= batch_norm[:, None]
        return batch
        
    def inverse_transform(self, batch):
        return batch * self.scaling_factor \
                if self.normalize_data else batch
    
    def calculate_scaling_factor(self, data_loader):
        print(f'Calculating norm mean of training set')
        norms = []
        self.model.eval()
        n_batches = len(data_loader)
        for batch_idx, (data, _) in enumerate(data_loader):
            batch_size = len(data)
            flattened_batch = data.view(batch_size, -1)
            batch_norm = flattened_batch.norm(dim=1, p=2)
            norms.extend(list(batch_norm.numpy()))
        norms = pd.Series(norms)
        print(norms.describe())
        self.scaling_factor = norms.mean()
        print('Done!\n')
    
    
    # Run training iterations and report results
    def train(self, train_loader, epoch, logging_func=print):
        self.model.train()
        train_loss = 0
        for batch_idx, (data, _) in enumerate(train_loader):
            data = self.transform(data).to(self.device)
            loss = self.step(data, train=True)
            train_loss += loss
            if batch_idx % self.log_interval == 0:
                logging_func('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}' \
                      .format(epoch, batch_idx * len(data), 
                              len(train_loader.dataset),
                              100. * batch_idx / len(train_loader),
                              loss / len(data)))

        logging_func('====> Epoch: {} Average loss: {:.4f}'.format(
              epoch, train_loss / len(train_loader.dataset)))
        
        
    # Returns the VLB for the test set
    def test(self, test_loader, epoch, logging_func=print):
        self.model.eval()
        test_loss = 0
        with torch.no_grad():
            for data, _ in test_loader:
                data = self.transform(data).to(self.device)
                test_loss += self.step(data, train=False)
                
        VLB = test_loss / len(test_loader)
        ## Optional to normalize VLB on testset
        name = self.model.__class__.__name__
        test_loss /= len(test_loader.dataset) 
        logging_func(f'====> Test set loss: {test_loss:.4f} - VLB-{name} : {VLB:.4f}')
        return test_loss
    
    
    #Auxiliary function to continue training from last trained models
    def load_last_model(self, checkpoints_path, logging_func=print):
        name = self.model.__class__.__name__
        # Search for all previous checkpoints
        models = glob(f'{checkpoints_path}/*.pth')
        model_ids = []
        for f in models:
            # modelname_dataset_startepoch_epochs_latentsize_lr_epoch
            run_name = Path(f).stem
            model_name, dataset, _, _, latent_sz, _, epoch = run_name.split('_')
            if model_name == name and dataset == self.dataset and \
               int(latent_sz) == self.latent_sz:
                model_ids.append((int(epoch), f))
                
        # If no checkpoints available
        if len(model_ids) == 0:
            logging_func(f'Training {name} model from scratch...')
            return 1

        # Load model from last checkpoint 
        start_epoch, last_checkpoint = max(model_ids, key=lambda item: item[0])
        logging_func('Last checkpoint: ', last_checkpoint)
        self.model.load_state_dict(torch.load(last_checkpoint))
        logging_func(f'Loading {name} model from last checkpoint ({start_epoch})...')

        return start_epoch + 1
    
    
    def update_(self):
        pass
    
    
    def run_training(self, train_loader, test_loader, epochs, 
                     report_interval, sample_sz=64, reload_model=True,
                     checkpoints_path='../results/checkpoints',
                     logs_path='../results/logs',
                     images_path='../results/images',
                     logging_func=print, start_epoch=None):
        
        if self.normalize_data:
            self.calculate_scaling_factor(train_loader)
        
        if start_epoch is None:
            start_epoch = self.load_last_model(checkpoints_path, logging_func) \
                                           if reload_model else 1
        name = self.model.__class__.__name__
        run_name = f'{name}_{self.dataset}_{start_epoch}_{epochs}_' \
                   f'{self.latent_sz}_{str(self.lr).replace(".", "-")}'
        logger = Logger(f'{logs_path}/{run_name}')
        logging_func(f'Training {name} model...')
        for epoch in range(start_epoch, start_epoch + epochs):
            train_loss = self.train(train_loader, epoch, logging_func)
            test_loss = self.test(test_loader, epoch, logging_func)
            # Store log
            logger.scalar_summary(train_loss, test_loss, epoch)
            # Optional update
            self.update_()
            # For each report interval store model and save images
            if epoch % report_interval == 0:
                with torch.no_grad():
                    ## Generate random samples
                    sample = torch.randn(sample_sz, self.latent_sz) \
                                  .to(self.device)
                    sample = self.model.decode(sample).cpu()
                    sample = self.inverse_transform(sample)
                    ## Store sample plots
                    save_image(sample.view(sample_sz, self.channels, self.height,
                                           self.width),
                               f'{images_path}/sample_{run_name}_{epoch}.png')
                    ## Store Model
                    torch.save(self.model.state_dict(), 
                               f'{checkpoints_path}/{run_name}_{epoch}.pth')

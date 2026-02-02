import numpy as np
import torch
import os

class NoEarlyStopping:
    def __init__(self, save_every_epoch=False, save_every_epoch_path=None, seed=None, verbose=False):
        self.epoch = 1
        self.seed = seed
        self.save_every_epoch = save_every_epoch
        self.save_every_epoch_path = save_every_epoch_path
        self.verbose = verbose
        self.early_stop = False

    def __call__(self, val_loss, model, path):

        # No early stopping logic (always save the model from the last epoch)
        self.save_checkpoint(val_loss, model, path)
        # Increment the epoch counter
        self.epoch += 1

    def save_checkpoint(self, val_loss, model, path):
        if self.verbose:
            print('Checkpoint model ...')
            print(f"Epoch: {self.epoch}")
            print(f"Save Every Epoch: {self.save_every_epoch}")
        # Save the model state every epoch
        torch.save(model.state_dict(), path + '/' + 'checkpoint.pth')

        # Save the model state every epoch if specified
        if self.save_every_epoch:
            # Create the directory if it doesn't exist
            if not os.path.exists(self.save_every_epoch_path):
                os.makedirs(self.save_every_epoch_path)

            # If a seed is provided, create a subdirectory for it
            if self.seed is not None:
                save_path = self.save_every_epoch_path + str(self.seed) + "/"
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                # Save the model state with the seed and epoch in the path
                torch.save(model.state_dict(), save_path + '/model_e' + str(self.epoch) + '.pth')
            else:
                # Save the model state with the epoch in the path
                torch.save(model.state_dict(), self.save_every_epoch_path + '/model_e' + str(self.epoch) + '.pth')

    
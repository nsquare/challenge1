import numpy as np
#import pickle


    
    
class DataPreProc(object):
    """Class for generating batch as (input, target) tuple
    
    """
    
    def __init__(self, batch_size, dic_cont_arr, shuffle = True, rand_seed = np.random.randint(100), input_transformations = None, target_transformations = None):
        self.batch_size = batch_size
        self.rand_seed = rand_seed
        self.shuffle = shuffle
        self.dic_count_arr = dic_cont_arr
        self.input = []
        self.target = []

        for inp, targ in self.dic_count_arr:
            self.input.append(inp)
            self.target.append(targ)
        
    def generate_batch(self):
        self.whole_batch = self.dic_count_arr
        if self.shuffle:
            np.random.shuffle(self.whole_batch) # In place shuffle
        end = len(self.whole_batch)-1
        last_idx = 0
        self.batch =[]
        if self.batch_size > end:
            #self._batch_idx = [0]
            self.batch.append(self.whole_batch)
            
        else:

            self._batch_idx = range(int(len(self.whole_batch)/self.batch_size))
            for idx in self._batch_idx:
                if last_idx <= end:
                    self.batch.append(self.whole_batch[last_idx:last_idx + self.batch_size])
                    last_idx = last_idx + self.batch_size
        return self.batch
    
    def input_transform(self):
        """
        TODO : add transformations on input array
        """
        return self.input
    
    def target_transform(self):
        """
        TODO : add transformations on target array
        """
        return self.target
    
    
    
#with open('./output/dic_cont_arr.pkl', 'rb') as handle:
#    dic_cont_arr = pickle.load(handle)

    

        
        
        
        
        
                
        
        
            

            
        


import configparser
import os
import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration,Adafactor
import glob
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd


#读取配置文件
pro_dir = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(pro_dir, "config.ini")
#if not os.path.exists(config_path):print("无配置文件")
config = configparser.ConfigParser()
config.read(config_path)
path_dataset = config.get("config","WebNLG_dataset")
path_savedTriple = config.get("config","dataset_triple_saveTo_csv")
path_entireModel = config.get("config","T5_pretrained_model")
path_testModel = config.get("config","T5_test_model")


# getData
files = glob.glob(path_dataset, recursive=True) 

print(len(files))
triple_re=re.compile('(\d)triples')
data_dct={}
for file in files:

    tree = ET.parse(file)
    root = tree.getroot()
    triples_num=int(triple_re.findall(file)[0])

    for sub_root in root:
        for ss_root in sub_root:
            strutured_master=[]
            unstructured=[]
            for entry in ss_root:
                unstructured.append(entry.text)
                strutured=[triple.text for triple in entry]
                strutured_master.extend(strutured)
            unstructured=[i for i in unstructured if i.replace('\n','').strip()!='' ]
            strutured_master=strutured_master[-triples_num:]
            strutured_master_str=(' && ').join(strutured_master)
            data_dct[strutured_master_str]=unstructured
mdata_dct={"prefix":[], "input_text":[], "target_text":[]}
for st,unst in data_dct.items():
    for i in unst:
        mdata_dct['prefix'].append('webNLG')
        mdata_dct['input_text'].append(st)
        mdata_dct['target_text'].append(i)


df=pd.DataFrame(mdata_dct)
df.to_csv(path_savedTriple)

train_df=pd.read_csv(path_savedTriple, index_col=[0])
train_df=train_df.iloc[  :35000,:]
train_df=train_df.sample(frac = 1)
batch_size=8
num_of_batches=len(train_df)/batch_size

tokenizer = T5Tokenizer.from_pretrained('t5-base')
model = T5ForConditionalGeneration.from_pretrained('t5-base',
                                             return_dict=True)

optimizer = Adafactor(model.parameters(),lr=1e-3,
                      eps=(1e-30, 1e-3),
                      clip_threshold=1.0,
                      decay_rate=-0.8,
                      beta1=None,
                      weight_decay=0.0,
                      relative_step=False,
                      scale_parameter=False,
                      warmup_init=False)


# from IPython.display import HTML, display

# def progress(loss,value, max=100):
#     return HTML(""" Batch loss :{loss}
#         <progress    
# value='{value}'max='{max}',style='width: 100%'>{value}
#         </progress>
#             """.format(loss=loss,value=value, max=max))

# import matplotlib.pyplot as plt
# import matplotlib.animation as anim


# y = []
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)

# def update(i):
#     yi = 1
#     y.append(yi)
#     x = range(len(y))
#     ax.clear()
#     ax.plot(x, y)
#     print(i, ': ', yi)

# a = anim.FuncAnimation(fig, update, frames=100, repeat=False)
# plt.show()






num_of_epochs = 1



model.train()

loss_per_10_steps=[]
for epoch in range(1,int(num_of_epochs)+1):
    print('Running epoch: {}'.format(epoch))
    
    running_loss=0
    # out = display(progress(1, num_of_batches+1), display_id=True)

    for i in range(int(num_of_batches)):
        inputbatch=[]
        labelbatch=[]
        new_df=train_df[i*batch_size:i*batch_size+batch_size]
        for indx,row in new_df.iterrows():
            input = 'WebNLG: '+row['input_text']+'</s>' 
            labels = row['target_text']+'</s>'   
            inputbatch.append(input)
            labelbatch.append(labels)
        inputbatch=tokenizer.batch_encode_plus(inputbatch,padding=True,max_length=400,return_tensors='pt')["input_ids"]
        labelbatch=tokenizer.batch_encode_plus(labelbatch,padding=True,max_length=400,return_tensors="pt") ["input_ids"]


        # clear out the gradients of all Variables 
        optimizer.zero_grad()

        # Forward propogation
        outputs = model(input_ids=inputbatch, labels=labelbatch)
        loss = outputs.loss
        loss_num=loss.item()
        logits = outputs.logits
        running_loss+=loss_num
        if i%10 ==0:      
            loss_per_10_steps.append(loss_num)
        # out.update(progress(loss_num,i, num_of_batches+1))
        print(loss_num,i, num_of_batches+1)

        # calculating the gradients
        loss.backward()

        #updating the params
        optimizer.step()
    
    running_loss=running_loss/int(num_of_batches)
    print('Epoch: {} , Running loss: {}'.format(epoch,running_loss))

    torch.save(model, path_testModel)



# Load Model
model_saved = torch.load(path_testModel)


import warnings
warnings.filterwarnings("ignore")

def generate(text,model,tokenizer):
    model.eval()
    input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), 
                                        return_tensors="pt")  
    # input_ids  = input_ids.to(dev)
    outputs = model.generate(input_ids)
    return tokenizer.decode(outputs[0])


text = generate('Lindsay | hobby | hiking ', model, tokenizer)
print(text)







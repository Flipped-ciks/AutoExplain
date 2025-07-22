import pymysql
import torchvision
import pandas as pd
from datasets import Dataset
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sklearn.model_selection import train_test_split
from transformers import TrainingArguments, Trainer

torchvision.disable_beta_transforms_warning()

def load_data_from_db():
    # 连接数据库
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="abc123",
        database="xkwdatabase"
    )

    query = """
    SELECT qid, stem, options, answer, original, final
    FROM questions
    """

    data = pd.read_sql(query, connection)
    connection.close()
    return data

def format_data(data):
    formatted_data = []
    for _, row in data.iterrows():
        input_text = f"题干: {row['stem']} 选项: {row['options']} 答案: {row['answer']} 解析: {row['original']}"
        target_text = row['final']
        formatted_data.append({"input": input_text, "target": target_text})
    return formatted_data

from torch.utils.data import Dataset

class QuestionDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=512):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        inputs = self.tokenizer(
            item['input'], max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt"
        )
        targets = self.tokenizer(
            item['target'], max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt"
        )
        return {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze(),
            "labels": targets["input_ids"].squeeze(),
        }


model_name = "t5-small"  # 可选择更大的模型如 t5-base 或 t5-large
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)



data = load_data_from_db()
formatted_data = format_data(data)

train_data, val_data = train_test_split(formatted_data, test_size=0.1, random_state=42)

train_dataset = QuestionDataset(train_data, tokenizer)
val_dataset = QuestionDataset(val_data, tokenizer)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
)

trainer.train()

def generate_analysis(stem, options, answer, original):
    input_text = f"题干: {stem} 选项: {options} 答案: {answer} 解析: {original}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


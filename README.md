<div align="center">

<h1>[ACM MM2025]Celeb Attributes Portfolio</h1>
  
<div>
  Jinjie Shen<sup>1</sup></a>
  Yaxiong Wang<sup>1</sup></a>
  Lechao Chen<sup>1</sup></a>
  Pu Nan<sup>2</sup></a>
  Zhun Zhong<sup>1</sup></a>
</div>

<div>
    <sup>1</sup>Hefei University of Technology
    <br>
    <sup>2</sup> University
</div>
</div>

## Introduction

We present <b>CAP</b>, a large-scale database including over 80k celebrities. Each celebrity in the CAP has three associated images along with their gender, birth year, occupation, and main achievements.

Two examples from CAP:

<div align="center">
<img src='./cap.png' width='40%'>
</div>

We provide the Python script `import_cap.py` that automatically integrates CAP information into your custom dataset by identifying all public celebrities mentioned in the textual content of each entry and incorporating their corresponding information.
## Quick start

### 🔧Format Requirements

- The file must be a **JSON array** (i.e., a list of objects).
- Every object must contain a `"text"` field.

### 📄 Example JSON File

```json
[
  {
    "id": "001",
    "text": "Julian Assange leaving court after his application for bail Journalists tweeted updates while the hearing was in progress",
    "other_info": "...",
     "..."
  },
  {
    "id": "002",
    "text": "Little Mix and mentor Tommy Gunn were nt expecting to win The X Factor",
    "tags": ["example", "test"],
    "..."
  }
]
```

### ⏬ Download CAP

For the convenience of downloading and usage, we provide two download options for CAP: Hugging Face and Baidu Pan, which include folders `people_imgs1`, `people_imgs2` and the json file `cap_texts.json`. Please move all data from the two folders ( `people_imgs1` and `people_imgs2` ) into the `people_imgs` folder.  [CAP HF](https://huggingface.co/datasets/SJJ0854/CAP) | [CAP Baidu Pan]()

### 🚀 Run script

Modify and run:

```
python import_cap.py \
  --path_A "/path/to/your/dataset.json" \
  --path_B "/path/to/cap_texts.json" \
  --folder_path "/path/to/people_imgs" \
  --output_path "/path/to/output.json"
```

📄 Example after running

```json
[
  {
    "id": "001",
    "text": "Julian Assange leaving court after his application for bail Journalists tweeted updates while the hearing was in progress",
    "other_info": "...",
    "cap_texts": {"Julian Assange": "Gender: Male, Occupation: Journalist, Birth year: 1971, Main achievement: Founder of WikiLeaks."},
    "cap_images": {"Julian Assange": ".../people_imgs/Julian Assange"},
     "..."
  },
  {
    "id": "002",
    "text": "Little Mix and mentor Tommy Gunn were nt expecting to win The X Factor",
    "tags": ["example", "test"],
    "cap_texts": {"Little Mix": "Gender: Female, Occupation: Singers, Birth year: NONE, Main achievement: British girl group formed in 2011."},
    "cap_images": {"Little Mix": ".../people_imgs/Little Mix"},
    "..."
  }
]
```

## 🤗🤗🤗 Citation

If you find this work useful for your research, please kindly cite our paper:


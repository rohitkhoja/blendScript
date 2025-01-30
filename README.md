# Run Blend Sql on your dataset


## Setup
1. Clone the repository:
   ```
   git clone https://github.com/parkervg/blendsql.git
   ```

2. Install dependencies:
   ```
   pip3 install typeguard
   pip3 install colorama
   pip3 install tabulate
   pip3 install fiscalyear
   pip3 install guidance
   pip3 install azure
   pip3 install azure-identity
   pip3 install guidance
   pip3 install sqlglot==18.1.0
   pip3 install rapidfuzz
   pip3 install diskcache 
   pip install skrub
   ```
3. clone this repository:
   ```
   https://github.com/rohitkhoja/blendScript.git
   ```
5. Run on local:
   ```
    export PYTHONPATH=/your/path/to/repo/blendsql:$PYTHONPATH
    python3 main.py
    # call function execute_blend(table, question, table_name, table_id) from main.py
   ```

## WikiTQ Dataset few shot examples
use file blendPrompt.txt

## Citation
   ```
      @article{glenn2024blendsql,
      title={BlendSQL: A Scalable Dialect for Unifying Hybrid Question Answering in Relational Algebra},
      author={Parker Glenn and Parag Pravin Dakle and Liang Wang and Preethi Raghavan},
      year={2024},
      eprint={2402.17882},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
   }
  ```

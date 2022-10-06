# Complex Network Attack Simulator

- [Complex Network Attack Simulator](#complex-network-attack-simulator)
  - [1. What's this?](#1-whats-this)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Demo dataset](#3-demo-dataset)
  - [4. Quick start](#4-quick-start)
  - [5. Main APIs](#5-main-apis)
  - [6. Attack types](#6-attack-types)
    - [6.1 Node attack](#61-node-attack)
      - [6.1.1 Shocks via node removal](#611-shocks-via-node-removal)
      - [6.1.2 Shocks via node perturbation](#612-shocks-via-node-perturbation)
    - [6.2 Edge attack](#62-edge-attack)
      - [6.2.1 Shocks via edge removal](#621-shocks-via-edge-removal)
      - [6.2.2 Shocks via edge perturbation](#622-shocks-via-edge-perturbation)
  - [Email me](#email-me)

## 1. What's this?

This is a repository for simulation of complex network attack in Python with NetworkX.

## 2. Prerequisites

Basic Python coding and complex network analysis. Some object-oriented programming would be good for understanding the source code.

## 3. Demo dataset

This dataset is synthetic and simplified for showing the core of code. It is csv format and has four columns, including source, target, value, and date.

## 4. Quick start
```python
from cnas.simulate import AttackSimulator
from cnas.metrics import directed_global_efficiency

data = pd.read_csv("./data/data.csv")
sim = AttackSimulator(
    data=data,
    head="exporter",
    tail="importer",
    weight="volume",
    group_id="year",
    how="edge",
    # random=False,
    random=True,
    iter_n=3,
    metrics=[nx.average_clustering, nx.transitivity, directed_global_efficiency]
)

result = sim.attack(ratio=0.5)

print(result)
```

## 5. Main APIs


## 6. Attack types

### 6.1 Node attack

#### 6.1.1 Shocks via node removal

#### 6.1.2 Shocks via node perturbation

### 6.2 Edge attack

#### 6.2.1 Shocks via edge removal

#### 6.2.2 Shocks via edge perturbation

## Email me
If you have any question or better idea for this repository, feel free to contact me!
<ml.liaoyuhua@gmail.com>

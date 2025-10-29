# GE5223 - NYC农贸市场与绅士化分析

## 项目概述

本项目旨在分析纽约市农贸市场与社区绅士化之间的关系。通过空间统计分析和时间序列分析，探索农贸市场密度与社区租金增长、收入变化等绅士化指标之间的相关性。

## 研究问题

1. **空间识别**: 农贸市场在纽约市的空间分布特征
2. **绅士化时间分析**: 社区绅士化进程的时间变化
3. **农贸市场时间分析**: 农贸市场数量和分布的时间变化
4. **相关性分析**: 农贸市场与绅士化之间的统计关系
5. **影响因素**: 影响这种关系的各种因素

## 数据来源

### 主要数据

1. **农贸市场数据**
   - NYC Farmers Markets (2009-2023) - NYC Open Data
   - Historical Farmers Markets (2009-2020) - Excel格式

2. **地理边界数据**
   - NYC Borough Boundaries - 区界数据
   - NYC Census Blocks (2000, 2020) - 人口普查区块数据

3. **经济人口数据**
   - NHGIS人口普查数据 (1990-2023) - 区块组级别
   - 消费者价格指数 (CPI) 数据 (1990-2024)

## 数据使用说明

#### **1. 农贸市场数据**
- **文件**:
  - `DataDictionary2023FarmersMarkets.xlsx`: 2023年农贸市场数据字典，包含字段定义和说明。
  - `Historical_FarmersMarkets_2009-2020.xlsx`: 2009-2020年历史农贸市场数据，包含时间序列和空间分布信息。
- **来源**: [NYC Open Data](https://data.cityofnewyork.us/Health/NYC-Farmers-Markets/8vwk-6iz2)
- **用途**:
  - 分析农贸市场的时空分布变化。
  - 结合人口普查数据，研究农贸市场与社区经济指标的关系。
- **字段说明**:
  - `Market Name`: 农贸市场名称。
  - `Location`: 地理位置（经纬度或地址）。
  - `Year`: 数据年份。
  - `Operational Status`: 运营状态（活跃/关闭）。

#### **2. 人口普查数据（NHGIS）**
- **目录**: `nhgis0003_shape/`
  - `nhgis0003_blockgroupcsv/`: 区块组级别的CSV数据（1990-2023年）。
    - 文件命名规则: `nhgis0003_ds[数据集编号]_[年份]_blck_grp.csv`
    - 示例: `nhgis0003_ds172_2010_blck_grp.csv`（2010年区块组数据）。
  - `nhgis0003_codebook/`: 数据字典文件，解释字段含义。
  - `nhgis0003_shape/`: 地理边界形状文件（ZIP格式）。
- **来源**: [NHGIS Data Finder](https://data2.nhgis.org/downloads)
- **用途**:
  - 分析人口、收入、租金等社区指标的变化。
  - 与农贸市场数据结合，研究绅士化趋势。
- **关键字段**:
  - `Total Population`: 总人口。
  - `Median Household Income`: 家庭收入中位数。
  - `Average Rent`: 平均租金。
  - `Geographic Identifier`: 地理单元唯一标识符（用于空间关联）。

#### **3. CPI数据（通胀调整）**
- **文件**: `CPI-U_Annual_Average_1990-2024.csv`
- **来源**: [美国劳工统计局 (BLS)](https://www.bls.gov/cpi/)
- **用途**:
  - 对经济指标（如收入、租金）进行通胀调整，确保跨年份数据可比性。
- **字段说明**:
  - `Year`: 年份。
  - `CPI-U`: 消费者价格指数（年度平均值）。
  - `Inflation Factor`: 通胀调整系数（可选）。

#### **4. 地理边界数据**
- **文件**: 
  - `nyc_boundaries_borough`: 纽约市区界数据。
  - `nyc_boundaries_blockgroup`: 人口普查区块组边界。
- **来源**: [NYC Open Data](https://data.cityofnewyork.us)
- **用途**:
  - 空间分析的基础地理单元。
  - 可视化农贸市场与社区指标的分布关系。

### **数据预处理步骤**
1. **数据加载**:
   - 使用 `pandas` 读取CSV和Excel文件。
   - 使用 `geopandas` 加载形状文件。
2. **地理编码**:
   - 将农贸市场地址转换为经纬度（如未提供）。
3. **数据关联**:
   - 通过地理标识符将人口普查数据与地理边界关联。
4. **通胀调整**:
   - 使用CPI数据对经济指标进行标准化。

### **注意事项**
1. **大文件管理**:
   - NHGIS的区块级数据（如 `nhgis0003_ds172_2010_block.csv`）体积较大（4.3GB），建议分块处理。
2. **数据更新**:
   - 定期检查NYC Open Data和NHGIS的数据更新。
3. **路径配置**:
   - 在脚本中使用绝对路径，避免跨平台问题。

### 绅士化指标

- **租金**: 平均租金变化
- **收入**: 家庭收入变化
- **人口**: 人口结构变化
- **政策因素**: 分区地图、重新分区计划等

## 目录结构

```
GE5223/
├── data/                         # 数据文件
│   ├── CPI-U_Annual_Average_1990-2024.csv      # CPI数据
│   ├── DataDictionary2023FarmersMarkets.xlsx    # 农贸市场数据字典
│   ├── Historical_FarmersMarkets_2009-2020.xlsx   # 历史农贸市场数据
│   └── nhgis0003_shape/          # NHGIS人口普查数据
│       ├── nhgis0003_blockgroupcsv/     # 区块组CSV数据
│       ├── nhgis0003_codebook/          # 数据字典
│       └── nhgis0003_shape/             # 形状文件
├── docs/                         # 文档
├── scripts/                      # 分析脚本
├── visualization/                # 可视化文件
└── GE5223 NYC farmers market- gentrification analysis.md  # 项目分析文档
```

## 分析方法

### 空间统计分析
- **KDA (Kernel Density Analysis)**: 密度分析
- **SAC (Spatial Auto-Correlation)**: 空间自相关分析
- **中心迁移路径分析**

### 时间序列分析
- 农贸市场数量时间变化
- 社区经济指标时间变化
- 相关性分析

### 聚类分析
- 空间聚类识别
- 时间聚类分析

## 技术栈

- **编程语言**: Python
- **空间分析**: GeoPandas, PySAL
- **数据处理**: Pandas, NumPy
- **可视化**: Matplotlib, Seaborn, Folium
- **统计分析**: SciPy, StatsModels

## 项目分工

- clj
- cwq  
- xsx
- ybs

## 使用说明

### 环境设置
```bash
# 创建虚拟环境
python -m venv ge5223_env

# 激活虚拟环境
ge5223_env\Scripts\activate  # Windows
source ge5223_env/bin/activate  # macOS/Linux

# 安装依赖
pip install geopandas pandas numpy matplotlib seaborn folium scipy statsmodels
```

### 数据预处理
1. 加载农贸市场数据并进行地理编码
2. 处理人口普查数据并与空间单元关联
3. 使用CPI数据进行通胀调整
4. 数据清洗和标准化

### 分析流程
1. 空间分布分析
2. 时间序列分析
3. 相关性分析
4. 可视化展示

## 预期成果

1. **地图可视化**: 社区租金增长与农贸市场密度关系的散点图
2. **空间聚类识别**: 绅士化热点区域识别
3. **时间变化分析**: 2009-2023年期间的变化趋势
4. **统计报告**: 相关性分析和影响因素分析

## 参考资料

- [NYC Open Data](https://data.cityofnewyork.us)
- [NHGIS Data Finder](https://data2.nhgis.org/downloads)
- [Urban Displacement Project Methodology](https://www.urbandisplacement.org)
- [LocateNYC Documentation](https://locatenyc.io/documentation)
"""
time:2022年9月12日
description:汇总每天的论文信息，按研究方向分类
"""

import os
from collections import defaultdict

def read_from_md(path):
    """
    从mdw文件中读取相关信息
    """
    papers = defaultdict(dict)
    with open(path,mode = 'r',encoding='utf8') as f:
        paper= {}
        lines = [line for line in f.read().splitlines() if line.strip()]
        for index in range(len(lines)):
            if lines[index][0:2] == "标题":
                if paper:
                    paper['url'] = os.path.dirname(path)[2:]+f"/{paper.get('标题','None')}"
                    paper["url"] = paper["url"].replace(":"," ").replace(" ","%20")
                    papers[paper["方向"]][paper["标题"]] = paper
                paper = {}
            if "：" in lines[index]:
                info = lines[index].strip().split("：")
                paper[info[0]] = info[1].strip()

        paper['url'] = os.path.dirname(path)[2:]+f"/{paper.get('标题','None')}"
        paper["url"] = paper["url"].replace(" ","%20")
        papers[paper["方向"]][paper["标题"]] = paper
    return papers            
            

def paper_merger(papers1,papers2):
    """
    将papers1和papers2进行合并，其中papers1为主体
    """
    for classification,papers in papers2.items():
        for name,paper in papers.items():
            if papers1[classification].get(name,False):
                # 存在同名文件
                if isinstance(papers1[classification][name],list):
                    papers1[classification][name].append(paper)
                elif isinstance(papers1[classification][name],dict):
                    papers1[classification][name] = [papers1[classification][name],paper]
                else:
                    raise("存在相同名称的论文，且无法自动去重处理")
            else:
                # 不存在同名论文，直接保存即可
                papers1[classification][name] = paper
    return papers1

def generate_md(papers,savepath = "./summary.md"):
    """
    根据papers信息生成summary.md
    """
    with open(savepath,mode= 'w',encoding="utf8") as f:
        f.write("# 文献汇总\n")  # 一级标题
        for classification,subpapers in papers.items():
            f.write("\n\n")
            f.write(f"## {classification}\n") # 二级标题
            f.write("|序号|标题|作者|时间|期刊|\n|:-:|:-:|:-:|:-:|:-:|\n") 
            # 处理每个方向下的具体内容
            for index,(name,paper) in enumerate(subpapers.items()):
                if isinstance(paper,dict):
                    # 处理正常论文
                    f.write(f"|{index+1}| \
                        [{paper.get('标题','None')}]({paper['url']})| \
                         {paper.get('作者','None')}| \
                        {paper.get('发表时间','None')}| \
                        {paper.get('期刊','None')}|\n")

                elif isinstance(paper,list):
                    # 处理存在重复论文的情况
                    for spaper in paper:
                        f.write(f"|<span style='backgroud:red;'>{index+1}</span>|\
                            <span style='backgroud:red;'>[{spaper.get('标题','None')}]({paper['url']}) </span> | \
                            <span style='backgroud:red;'>{spaper.get('作者','None')}  </span> | \
                            <span style='backgroud:red;'>{spaper.get('发表时间','None')} </span> | \
                            <span style='backgroud:red;'>{spaper.get('期刊','None')} </span> |\n")

def summary_all(path="./"):
    """
    对所有文件进行汇总
    papers = {
        classification:{"name":{name:,author:,...}}
    }
    """
    papers = defaultdict(dict)
    for file in os.listdir(path):
        if not os.path.isdir(path+f"{file}") or file.startswith("."):
            continue
        paper = read_from_md(path+f"{file}/论文基本信息.md")   # 如何处理同名论文？按照规则来说，应当在文档中列出来标红，等待处理
        papers = paper_merger(papers,paper) #合并文档
    
    # 排序，先类内排序，在类间排序
    
    # 根据dict生成md文件，按照分类进行生成
    generate_md(papers)
    



if __name__ == "__main__":
    summary_all()




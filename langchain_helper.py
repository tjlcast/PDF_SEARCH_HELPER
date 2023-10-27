#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time 2023/10/27 S{TIME} 
# @Name langchain_helper. Py
# @Author：jialtang

import os

from langchain.document_loaders import PyPDFLoader
from langchain.indexes.vectorstore import VectorstoreIndexCreator, VectorStoreIndexWrapper
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma

load_dotenv()

file_path = "./zwd.pdf"

local_persist_path = "./vector_store"


# What the difference?
# index.query("唐嘉良发生了什么？")
# index.query_with_sources("唐嘉良发生了什么？", chain_type="map_reduce")


def get_index_path(index_name):
    return os.path.join(local_persist_path, index_name)


def load_pdf_and_save_to_index(file_path, index_name):
    loader = PyPDFLoader(file_path)
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": get_index_path(index_name)}).from_loaders([loader])
    index.vectorstore.persist()


def load_index(index_name):
    index_path = get_index_path(index_name)
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=index_path,
        embedding_function=embedding,
    )
    return VectorStoreIndexWrapper(vectorstore=vectordb)


def query_index_lc(index, query):
    ans = index.query_with_sources(query, chain_type="map_reduce")
    return ans['answer']

# test
# load_pdf_and_save_to_index(file_path, "text")
# index = load_index("text")
# ans = index.query_with_sources("唐嘉良发生了什么？", chain_type="map_reduce")
# print(ans)

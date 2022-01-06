# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# <img align="right" src="images/tf.png"/>
# <img align="right" src="images/etcbc.png"/>
# <img align="right" src="images/logo.png"/>
#
# # Search Introduction
#
# *Search* in Text-Fabric is a template based way of looking for structural patterns in your dataset.
#
# Within Text-Fabric we have the unique possibility to combine the ease of formulating search templates for
# complicated syntactical patterns with the power of programmatically processing the results.
#
# This notebook will show you how to get up and running.
#
# ## Easy command
#
# Search is as simple as saying (just an example)
#
# ```python
# results = A.search(template)
# A.show(results)
# ```
#
# See all ins and outs in the
# [search template docs](https://annotation.github.io/text-fabric/tf/about/searchusage.html).

# # Incantation
#
# The ins and outs of installing Text-Fabric, getting the corpus, and initializing a notebook are
# explained in the [start tutorial](start.ipynb).

# %load_ext autoreload
# %autoreload 2

import unicodedata
from tf.app import use

A = use("athenaeus:clone", checkout="clone", hoist=globals())
# A = use('athenaeus', hoist=globals())

# # Basic search command
#
# We start with the most simple form of issuing a query.
# Let's look for the words in book 3, chapter 4.
#
# All work involved in searching takes place under the hood.

query = """
book book=3
  chapter chapter=4
    word
"""
results = A.search(query)
A.table(results, end=10, skipCols="1 2")

# The hyperlinks take us all to the beginning of the book of Matthew.
#
# Note that we can choose start and/or end points in the results list.

A.table(results, start=8, end=13, skipCols="1 2")

# We can show the results more fully with `show()`.

A.show(results, start=8, end=13, skipCols="1 2")


# Before we go on, there is a thing with Unicode.
#
# All Greek strings in this corpus are in decomposed normal form. That means e.g. that
# `ἐπί` has 5 letters.
#
# However, when this string is printed in a Jupyter notebook, it is converted to composed normal form.
# So when we copy and paste such a string in a query, we must make sure that we paste the denormalized form.
#
# We use a utility function for that:


def ud(s):
    return unicodedata.normalize("NFD", s)


query = f"""
word lemma={ud('ἐπί')}
"""
results = A.search(query)
A.show(results, condenseType="_sentence", condensed=True, end=5)

A.table(results, end=10)

query = """
word lemma=*ακαδημαικων
"""
results = A.search(query)
A.show(results, condenseType="_sentence", end=5)

# ---
#
# CC-BY Dirk Roorda
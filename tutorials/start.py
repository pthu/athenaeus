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

# <img align="right" src="images/tf.png" width="128"/>
# <img align="right" src="images/dans.png"/>
# <img align="right" src="images/logo.png"/>
#
# # Tutorial
#
# This notebook gets you started with using
# [Text-Fabric](https://annotation.github.io/text-fabric/) for coding in the Athenaeus corpus.
#
# Familiarity with the underlying
# [data model](https://annotation.github.io/text-fabric/tf/about/datamodel.html)
# is recommended.

# ## Installing Text-Fabric
#
# ### Python
#
# You need to have Python on your system. Most systems have it out of the box,
# but alas, that is python2 and we need at least python **3.6**.
#
# Install it from [python.org](https://www.python.org) or from
# [Anaconda](https://www.anaconda.com/download).
#
# ### TF itself
#
# ```
# pip3 install text-fabric
# ```
#
# ### Jupyter notebook
#
# You need [Jupyter](http://jupyter.org).
#
# If it is not already installed:
#
# ```
# pip3 install jupyter
# ```

# ## Tip
# If you start computing with this tutorial, first copy its parent directory to somewhere else,
# outside your `syrnt` directory.
# If you pull changes from the `syrnt` repository later, your work will not be overwritten.
# Where you put your tutorial directory is up till you.
# It will work from any directory.

# %load_ext autoreload
# %autoreload 2

import collections

from tf.app import use

# ## Corpus data
#
# Text-Fabric will fetch the Athenaeus corpus for you.
#
# It will fetch the newest version by default, but you can get other versions as well.
#
# The data will be stored in the `text-fabric-data` in your home directory.
#

# # Features
# The data of the corpus is organized in features.
# They are *columns* of data.
# Think of the text as a gigantic spreadsheet, where row 1 corresponds to the
# first word, row 2 to the second word, and so on, for all 300,000 words.
#
# Each piece of information about the words, including the text of the words, constitute a column in that spreadsheet.
#
# Instead of putting that information in one big table, the data is organized in separate columns.
# We call those columns **features**.

# # Incantation
#
# The simplest way to get going is by this *incantation*:

# For the very last version, use `hot`.
#
# For the latest release, use `latest`.
#
# If you have cloned the repos (TF app and data), use `clone`.
#
# If you do not want/need to upgrade, leave out the checkout specifiers.

A = use("athenaeus:clone", checkout="clone", hoist=globals())
# A = use('athenaeus:hot', checkout="hot", hoist=globals())
# A = use('athenaeus:latest', checkout="latest", hoist=globals())
# A = use('athenaeus', hoist=globals())

# You can see which features have been loaded, and if you click on a feature name, you find its documentation.
# If you hover over a name, you see where the feature is located on your system.
#
# Edge features are marked by **_bold italic_** formatting.
#
# There are ways to tweak the set of features that is loaded. You can load more and less.
#
# See [share](share.ipynb) for examples.

# # Counting

# +
A.indent(reset=True)
A.info("Counting nodes ...")

i = 0
for n in N.walk():
    i += 1

A.info("{} nodes".format(i))
# -

# # Node types

F.otype.slotType

F.otype.all

C.levels.data

for (typ, av, start, end) in C.levels.data:
    print(f"{end - start + 1:>7} {typ}s")

# # Feature statistics

# There are no linguistic features, as far as I can see, but there is `lemma`.

# # Word matters
#
# ## Top 20 frequent words

for (w, amount) in F.lemma.freqList("word")[0:20]:
    print(f"{amount:>5} {w}")

# ## Hapaxes

hapaxes1 = sorted(lx for (lx, amount) in F.lemma.freqList("word") if amount == 1)
len(hapaxes1)

for lx in hapaxes1[0:20]:
    print(lx)

# ### Small occurrence base
#
# The occurrence base of a word are the books in which the word occurs.

# +
occurrenceBase = collections.defaultdict(set)

A.indent(reset=True)
A.info("compiling occurrence base ...")
for s in F.otype.s("book"):
    book = F.book.v(s)
    for w in L.d(s, otype="word"):
        occurrenceBase[F.lemma.v(w)].add(book)
A.info("done")
A.info(f"{len(occurrenceBase)} entries")
# -

# An overview of how many words have how big occurrence bases:

# +
occurrenceSize = collections.Counter()

for (w, books) in occurrenceBase.items():
    occurrenceSize[len(books)] += 1

occurrenceSize = sorted(
    occurrenceSize.items(),
    key=lambda x: (-x[1], x[0]),
)

for (size, amount) in occurrenceSize[0:10]:
    print(f"books {size:>4} : {amount:>5} words")
print("...")
for (size, amount) in occurrenceSize[-10:]:
    print(f"books {size:>4} : {amount:>5} words")
# -

# Let's give the predicate *private* to those words whose occurrence base is a single book.

privates = {w for (w, base) in occurrenceBase.items() if len(base) == 1}
len(privates)

# ### Peculiarity of books
#
# As a final exercise with books, lets make a list of all books, and show their
#
# * total number of words
# * number of private words
# * the percentage of private words: a measure of the peculiarity of the book

# +
bookList = []

empty = set()
ordinary = set()

for d in F.otype.s("book"):
    book = F.book.v(d)
    words = {F.lemma.v(w) for w in L.d(d, otype="word")}
    a = len(words)
    if not a:
        empty.add(book)
        continue
    o = len({w for w in words if w in privates})
    if not o:
        ordinary.add(book)
        continue
    p = 100 * o / a
    bookList.append((book, a, o, p))

bookList = sorted(bookList, key=lambda e: (-e[3], -e[1], e[0]))

print(f"Found {len(empty):>4} empty books")
print(f"Found {len(ordinary):>4} ordinary books (i.e. without private words)")

# +
print(
    "{:<20}{:>5}{:>5}{:>5}\n{}".format(
        "book",
        "#all",
        "#own",
        "%own",
        "-" * 35,
    )
)

for x in bookList[0:20]:
    print("{:<20} {:>4} {:>4} {:>4.1f}%".format(*x))
print("...")
for x in bookList[-20:]:
    print("{:<20} {:>4} {:>4} {:>4.1f}%".format(*x))
# -

# # Next steps
#
# By now you have an impression how to compute around in the Athenaeus.
# While this is still the beginning, I hope you already sense the power of unlimited programmatic access
# to all the bits and bytes in the data set.
#
# Here are a few directions for unleashing that power.
#
# **(in progress, not all of the tutorials below exist already!)**
#
# * **[display]"(display.ipynb)"** become an expert in creating pretty displays of your text structures
# * **[search](search.ipynb)** turbo charge your hand-coding with search templates
# * **[exportExcel]"(exportExcel.ipynb)"** make tailor-made spreadsheets out of your results
# * **[share]"(share.ipynb)"** draw in other people's data and let them use yours
#
# CC-BY Dirk Roorda

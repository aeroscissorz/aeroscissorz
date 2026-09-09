---
title: How to make an AI agent understand your data
date: sep 9, 2026
words: 800
status: public
---

I was building an AI agent that could answer questions about company data.

The demo worked.

It could call tools, generate SQL, summarize results, and sound convincing.

That was the problem.

A convincing answer is not necessarily a correct answer.

The agent knew how to query a database. It did not know what the tables meant.

## A catalog is not just a list of tables

I started with Dataplex Universal Catalog. By the time I was working with it, Google had renamed it Knowledge Catalog. The name changed, but the existing Dataplex APIs, `gcloud dataplex` commands, and client libraries continued to work.

The new name made more sense. A catalog used to mean a searchable inventory of data assets. Knowledge Catalog was trying to become something more useful: a continuously updated context layer for both humans and AI agents.

## Starting with discovery

The first thing I wanted was a reliable inventory. Knowledge Catalog could harvest metadata from sources such as BigQuery, Cloud Storage, AlloyDB, Spanner, and Cloud SQL.

That gave me the technical layer: schemas, locations, ownership, update information, and relationships between assets.

But raw metadata is still raw metadata. A column named `rev` does not tell an agent whether it means revenue, revision, or reverse.

## Adding meaning to the metadata

I began writing descriptions for the assets that mattered most. What does this dataset represent? Which team owns it? What is the expected freshness? Which filters are always required?

The answers became part of the catalog instead of living in a document nobody opened.

Revenue, orders, customers, refunds, and subscriptions were no longer isolated words. They formed a shared vocabulary the agent could use when searching for relevant data.

## The query problem

Finding the right table was only half the job. The agent still had to write the right query.

This is where verified queries helped. A verified query is a known-good example of how a business question should be answered. It captures more than syntax. It captures intent.

> What was monthly recurring revenue for new customers in the previous quarter?

There may be several technically valid ways to write that query. Only one may match the company’s definition of recurring revenue.

I collected these examples and attached them to the relevant data context. Now the agent had more than a schema. It had patterns.

## Keeping governance in the path

The easiest way to make an agent useful is to give it access to everything. The easiest way to make that agent dangerous is also to give it access to everything.

Knowledge Catalog respects the permissions attached to the underlying assets. Search results and retrieved context are filtered by the caller’s access.

Permissions are stronger than reminders.

## The agent finally had a map

Once the catalog contained technical metadata, business descriptions, ownership, verified queries, and access controls, I connected it to the agent.

The biggest improvement was not that the model became smarter. The improvement was that it had somewhere reliable to look.

Knowledge Catalog is now the name Google uses for what used to be Dataplex Universal Catalog. For me, the rename described the real shift: from cataloging data to making data understandable to machines.

My agent did not need another giant system prompt.

It needed a shared source of truth.

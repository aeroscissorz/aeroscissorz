---
title: Your AI Agent Doesn't Need a Bigger Prompt. It Needs a Data Catalog.
date: sep 9, 2026
words: 1100
status: public
---

I was building an AI agent that could answer questions about company data.

It looked impressive.

It could call tools, generate SQL, execute queries, summarize results, and explain its reasoning.

Then I asked it a simple question:

> What was our monthly recurring revenue from new customers last quarter?

The SQL was valid.

The query ran successfully.

The answer was wrong.

That was the real problem.

**An AI agent can know how to query a database without understanding what the data means.**

## A database schema isn't enough

A database can tell an agent that a table contains:

```text
customers
orders
subscriptions
revenue
refunds
```

It can tell the model that `revenue` is a numeric column.

It cannot reliably tell the model what the company means by "revenue."

Does it include refunds?

Does it include test accounts?

Is recurring revenue calculated from invoices, subscriptions, or successful payments?

Does "new customer" mean the first purchase, first subscription, or first day the account was created?

These aren't SQL problems.

They're **context problems**.

And stuffing more instructions into the system prompt isn't a good solution.

## The catalog needs to become a context layer

I started with Dataplex Universal Catalog. By the time I was working with it, Google had renamed it **Knowledge Catalog**.

The name change actually captured what I needed.

I didn't just want an inventory of tables.

I wanted a place where the agent could discover:

- what data exists
- what it means
- who owns it
- how fresh it is
- how it should be queried
- which definitions are trusted
- who is allowed to access it

That turns the catalog from a directory into a **context layer**.

## Start with discovery

The first step was building a reliable inventory.

Knowledge Catalog can harvest metadata from sources such as BigQuery, Cloud Storage, AlloyDB, Spanner, and Cloud SQL.

That gives the agent useful technical information:

```text
Dataset
 ├── tables
 ├── columns
 ├── types
 ├── locations
 ├── ownership
 ├── relationships
 └── update information
```

This solves the discovery problem.

But it doesn't solve the meaning problem.

A column called:

```text
rev
```

could mean:

```text
revenue
revision
reverse
```

The schema alone doesn't know.

## Add meaning where the data lives

I started adding descriptions to the assets that mattered most.

Not generic descriptions.

Business meaning.

For example:

```yaml
dataset: customer_revenue

description: >
  Revenue generated from paying customers.
  Excludes refunds and internal test accounts.

owner: finance

freshness: daily

business_terms:
  recurring_revenue: >
    Subscription revenue expected to repeat
    on an ongoing basis.

  new_customer: >
    Customer whose first successful payment
    occurred during the measurement period.
```

Now the meaning isn't trapped inside someone's head, a Slack message, or a document nobody opens.

It becomes part of the data context the agent can retrieve.

That distinction matters.

**Metadata tells the agent what something is.  
Business context tells it what something means.**

## The query problem

Finding the right table was only half the problem.

The agent still had to write the right query.

This is where **verified queries** became useful.

A verified query is a known-good example of how a business question should be answered.

For example:

> What was monthly recurring revenue from new customers last quarter?

There can be several SQL queries that:

- compile
- execute
- return numbers
- look completely reasonable

Only one may match the company's definition of recurring revenue.

So instead of asking the model to invent the logic every time, I gave it examples.

Conceptually:

```yaml
question: >
  What was monthly recurring revenue
  from new customers last quarter?

dataset: customer_revenue

verified_query: |
  SELECT
    DATE_TRUNC(month, month) AS month,
    SUM(recurring_revenue) AS mrr
  FROM customer_revenue
  WHERE customer_type = 'new'
  GROUP BY month
  ORDER BY month;
```

The important part isn't the SQL itself.

The query captures **intent**.

It shows the agent how this organization answers this particular class of question.

The catalog now contains both:

```text
"What data exists?"
```

and:

```text
"How do we normally use this data?"
```

That is a much stronger form of context.

## Permissions are part of the context

There is another problem with giving an AI agent access to company data.

The easiest way to make an agent useful is to give it access to everything.

The easiest way to make that agent dangerous is also to give it access to everything.

Permissions therefore can't be an afterthought.

The catalog needs to respect the access controls of the underlying data.

A user shouldn't receive metadata or query context for data they aren't authorized to access simply because an LLM knows how to ask for it.

This leads to a principle I found more useful than adding another instruction to the prompt:

> **Permissions are stronger than reminders.**

Don't tell the model:

```text
Don't access sensitive data.
```

Enforce what it can actually discover and retrieve.

## The architecture

The resulting architecture became much simpler to reason about:

```text
                    USER
                      |
                      v
                  AI AGENT
                      |
                      v
              KNOWLEDGE CATALOG
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
     Metadata    Business       Verified
                  Meaning        Queries
        |             |             |
        +-------------+-------------+
                      |
                      v
                 Access Control
                      |
                      v
                  DATA SOURCES
```

The agent still generates SQL.

The difference is that it no longer has to reconstruct the organization's understanding of the data from a raw schema every time.

It has a map.

## The model didn't become smarter

This was the most interesting part.

The model didn't suddenly become better at SQL.

I didn't replace it with a larger model.

I didn't write an enormous system prompt containing every possible business rule.

I gave it better context.

Before:

```text
User
  ↓
LLM
  ↓
Database
```

After:

```text
User
  ↓
LLM
  ↓
Relevant data context
  ↓
Business definitions
  ↓
Verified examples
  ↓
Database
```

The second architecture gives the model something much more valuable than additional instructions:

**a source of truth.**

## What I would build differently from the start

If I were starting the agent again, I wouldn't begin with SQL generation.

I'd begin with the knowledge layer.

I'd define:

1. **What datasets exist?**
2. **What does each dataset mean?**
3. **Who owns it?**
4. **How fresh is it?**
5. **Which business terms map to which data?**
6. **Which queries have already been verified?**
7. **What can the current user access?**

Only after answering those questions would I ask the agent to generate SQL.

The SQL is the final step.

The difficult part is making sure the agent has enough information to generate the **right** SQL.

## The bigger lesson

AI agents are often described as if the main challenge is intelligence.

In production, the harder problem is frequently **context**.

A model can be excellent at reasoning and still produce a confidently wrong answer if the information it is reasoning over is incomplete or ambiguous.

That's why I think the future of AI data systems isn't just:

```text
LLM + tools
```

It's:

```text
LLM
+
tools
+
structured knowledge
+
business semantics
+
verified examples
+
governance
```

Knowledge Catalog is now the name Google uses for what used to be Dataplex Universal Catalog.

For me, the rename describes the more important shift:

**from cataloging data to making data understandable to machines.**

My agent didn't need another giant system prompt.

It needed a shared source of truth.

Sitemap
Open in app
Sign up
Sign in
Medium Logo
Write
Sign up
Sign in
## 
Databases
·
Follow publication
“Databases” is a publication dedicated to deepening your understanding of databases. From ACID principles to performance tuning, indexing and query optimization, we break down database concepts in a simple, practical way.
Follow publication
Member-only story
# The N+1 Database Query Problem: A Simple Explanation and Solutions
Sergey Egorenkov
Follow
3 min read
·
Feb 6, 2025
--
Listen
Share
If you work with databases and applications, you may have heard of the **N+1 problem**. It’s a common performance issue that happens when an application makes too many database queries instead of fetching data efficiently. This can slow down your app and make it harder to scale.
# What Is the N+1 Problem?
Imagine you have a list of students, and each student has multiple courses they are enrolled in. This is a one-to-many relationship because one student can have many courses.
Now, let’s say you need to get all students along with their courses. If your application is not optimized, it might do the following:
1. First, fetch all students:
```
SELECT * FROM students;
```

2. Then, for each student, fetch their courses one by one:
```
SELECT * FROM courses WHERE student_id = ?;
```

If you have 100 students, this results in 101 queries (1 query for students + 100 queries for courses). That’s why it’s called the **N+1 problem** — you run N (number of students) + 1 queries.
--
--
Follow
## Published in Databases
351 followers
·Last published May 3, 2025
“Databases” is a publication dedicated to deepening your understanding of databases. From ACID principles to performance tuning, indexing and query optimization, we break down database concepts in a simple, practical way.
Follow
Follow
## Written by Sergey Egorenkov
376 followers
·31 following
Senior Software Engineer. Writing about software development with deep insights & real-world experience. You can reach out to me via email: egsesmail@gmail.com.
Follow
## No responses yet
Write a response
What are your thoughts?
Cancel
Respond
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2Fp%2Fef11751aef8a&%7Efeature=LoOpenInAppButton&%7Echannel=ShowPostUnderCollection&%7Estage=mobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------
- egsesmail@gmail.com
- https://medium.statuspage.io/?source=post_page-----ef11751aef8a---------------------------------------
- pressinquiries@medium.com
- https://speechify.com/medium?source=post_page-----ef11751aef8a---------------------------------------
Sitemap
Open in app
Sign up
Sign in
Medium Logo
Write
Sign up
Sign in
Sergey Egorenkov
376 followers
Home
About
Published in
DevOps and Architecture
## Costs of Microservices You Should Know Before Breaking Up Your Monolith
### A practical look at the hidden trade-offs behind microservice architectures.
Jun 2
Jun 2
Published in
DevOps and Architecture
## Microservices Data Flow: Sync, Async, and Async That Scales
### So you’re building a content platform. Think Medium or Substack — users can publish articles, others can follow, like, comment, share…
May 28
May 28
Published in
CyberSecurity
## AI Can Hack Your App in Seconds. Here Is What You Can Do
### How AI is accelerating attacks — and what developers can do to defend their apps.
May 8
May 8
Published in
Databases
## Why NoSQL Was Invented (and Where SQL Failed Us)
### Exploring the architectural trade-offs that led to the rise of NoSQL systems.
May 3
A response icon1
May 3
A response icon1
Published in
CyberSecurity
## Refresh Tokens Are Trickier Than Many Developers Think
### It’s not enough to make them work, here’s how to make them secure, reliable, and hard to exploit.
Apr 30
Apr 30
Published in
CyberSecurity
## Why JWT Needs a Secret If It’s Not Encrypted
### This comes up more often than you’d expect…
Apr 30
Apr 30
Published in
Databases
## MVCC in Databases: How It Works and Why It’s Needed
### Why modern databases use MVCC and what it costs.
Apr 22
A response icon1
Apr 22
A response icon1
Published in
Toxic Engineering
## The Nonsense of JavaScript
### You should be ready for this when writing JavaScript.
Apr 12
A response icon3
Apr 12
A response icon3
Published in
Toxic Engineering
## Worst Node.js Practices to Use If You Want to Destroy Your App
### A guide to build a Node.js app engineered to destroy performance, security, and maintainability.
Apr 11
A response icon3
Apr 11
A response icon3
Published in
Toxic Engineering
## TypeScript: The Ball and Chain You Begged For
### A brutally honest look at the cost of TypeScript.
Apr 5
A response icon1
Apr 5
A response icon1
## Sergey Egorenkov
376 followers
Senior Software Engineer. Writing about software development with deep insights & real-world experience. You can reach out to me via email: egsesmail@gmail.com.
Follow
Following
  * DevOps and Architecture
  * CyberSecurity
  * Tac Tacelosky
  * Kevin Masur
  * XeusNguyen


See all (31)
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2F%40egorenkovserg&%7Efeature=LoOpenInAppButton&%7Echannel=ShowUser&%7Estage=mobileNavBar&source=---two_column_layout_nav-----------------------------------------
- egsesmail@gmail.com
- https://medium.statuspage.io/?source=user_profile_page---user_sidebar-------------------2ad674831bd----------------------
- pressinquiries@medium.com
- https://speechify.com/medium?source=user_profile_page---user_sidebar-------------------2ad674831bd----------------------
Sitemap
Medium Logo
Our story
Membership
Write
Sign in
Get started
## Human   
stories & ideas
### A place to read, write, and deepen your understanding
Start reading
Start reading
AboutHelpTermsPrivacy
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://medium.statuspage.io
- pressinquiries@medium.com
- https://speechify.com/medium
Sitemap
Open in app
Sign up
Sign in
Medium Logo
Write
Sign up
Sign in
# Recent searches
You have no recent searches
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://rsci.app.link/s1cSf8zJT3?%7Efeature=LoOpenInAppButton&%7Echannel=other&%7Estage=mobileNavBar&source=---two_column_layout_nav-----------------------------------------
- https://medium.statuspage.io/?source=search_post---two_column_layout_sidebar-----------------------------------------
- pressinquiries@medium.com
- https://speechify.com/medium?source=search_post---two_column_layout_sidebar-----------------------------------------
Sitemap
Open in app
Sign up
Sign in
Medium Logo
Write
Sign up
Sign in
Databases
Followers
## 350 followers
## Mehran Khan
Follow
## Vjekoslav Matausic
Follow
## marc
Follow
## devseop
Follow
## John P McAnulty
Data Specialist @ Google
Follow
## Patrick Erdelt
Follow
## Muhammad Iqbal Ali
Software Programmer — Backend Engineer
Follow
## Aniketnangare
Follow
## Vikas
Follow
## Karunesh
Follow
## Matija X Zivkovic
Follow
## Rinaldi Ferdiansyah
Follow
## Abuchi Okoloji
Follow
## Pydevink
Follow
## Hagen Hübel
Chief of data and vectors, CTO @ https://infobud.ai
Follow
## keith simpson
Follow
## Darsh Nahar 23BAI0087
Follow
## anon
Follow
## XD
Follow
## Juarez Junior
Developer Relations @ Oracle ☕️🥑 https://linktr.ee/juarezjunior
Follow
## Kennedy Mwenda
Full Stack and Language Agnostic Developer with interest in Desktop, Web and Mobile Applications.
Follow
## Steven L Levitt
Follow
## Amrutha Sunkara
Follow
## Sandis Kerve
Follow
## yanto moto
Follow
## Kanivel
Software Engineer,Mobile App Developer,Freelancer,Interested In Blockchain,AI,Machine Learning
Follow
## Leandro Mileski
Studying Financial Engineering | Quantitative Risk Management
Follow
## Ahmetsalihaymelek
Follow
## Jose Inziano
Follow
## Divyankpandey
Follow
## Sergey Egorenkov
Senior Software Engineer. Writing about software development with deep insights & real-world experience. You can reach out to me via email: egsesmail@gmail.com.
Follow
## Sh Ph
Follow


“Databases” is a publication dedicated to deepening your understanding of databases. From ACID principles to performance tuning, indexing and query optimization, we break down database concepts in a simple, practical way.
Follow
Connect with Databases
## Editors
## Sergey Egorenkov
Senior Software Engineer. Writing about software development with deep insights & real-world experience. You can reach out to me via email: egsesmail@gmail.com.
Follow
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://rsci.app.link/s1cSf8zJT3?%7Efeature=LoOpenInAppButton&%7Echannel=other&%7Estage=mobileNavBar&source=---two_column_layout_nav-----------------------------------------
- https://twitter.com/egorenkovserg?source=collection_followers_page---collection_sidebar-4ac4ff76014d----------------------------------------
- https://medium.statuspage.io/?source=collection_followers_page---collection_sidebar-4ac4ff76014d----------------------------------------
- pressinquiries@medium.com
- https://speechify.com/medium?source=collection_followers_page---collection_sidebar-4ac4ff76014d----------------------------------------
Homepage
Open in app
Sign inGet started
# DATABASES
Follow
Why NoSQL Was Invented (and Where SQL Failed Us)
### 
Why NoSQL Was Invented (and Where SQL Failed Us)
Exploring the architectural trade-offs that led to the rise of NoSQL systems.
Sergey Egorenkov
May 3
MVCC in Databases: How It Works and Why It’s Needed
### 
MVCC in Databases: How It Works and Why It’s Needed
Why modern databases use MVCC and what it costs.
Sergey Egorenkov
Apr 22
UUID vs Auto-Increment Integer for IDs. What you should choose
### 
UUID vs Auto-Increment Integer for IDs. What you should choose
Make the right decision when designing your database schema
Sergey Egorenkov
Apr 1
Why Uber Moved from Postgres to MySQL
### 
Why Uber Moved from Postgres to MySQL
How PostgreSQL’s architecture clashed with Uber’s scale — and why MySQL offered a better path forward
Sergey Egorenkov
Mar 28
Database Partitioning Disadvantages You Should Know
### 
Database Partitioning Disadvantages You Should Know
Partitioning Can Cause Problems — Understand Them Before Implementation
Sergey Egorenkov
Mar 21
Making SQL query 40x faster for 10 million rows table
### 
Making SQL query 40x faster for 10 million rows table
Make your SQL query really fast using this approach
Sergey Egorenkov
Mar 17
How to get complete analysis of your SQL query and how to read it
### 
How to get complete analysis of your SQL query and how to read it
Know more about your SQL queries and adjust your approach accordingly
Sergey Egorenkov
Mar 15
Row vs Column-Oriented Databases
### 
Row vs Column-Oriented Databases
Understanding the Key Differences, Strengths, and Use Cases of Row and Column-Oriented Databases
Sergey Egorenkov
Mar 12
How Database Indexes Work (In Simple Words)
### 
How Database Indexes Work (In Simple Words)
Learn how indexing is working and make your database queries much faster.
Sergey Egorenkov
Mar 1
4 Foundational Principles of Databases. ACID
### 
4 Foundational Principles of Databases. ACID
The Backbone of Reliable Transactions: Ensuring Integrity with ACID Principles
Sergey Egorenkov
Feb 18
Breaking Down the Anatomy of a Database Page
### 
Breaking Down the Anatomy of a Database Page
Database Page Structures: How Data is Organized and Retrieved
Sergey Egorenkov
Feb 7
The N+1 Database Query Problem: A Simple Explanation and Solutions
### 
The N+1 Database Query Problem: A Simple Explanation and Solutions
Understanding the N+1 Query Problem: How to Optimize Database Performance and Avoid Slow Queries
Sergey Egorenkov
Feb 5
Learning Databases? Don’t Overlook ACID Principles. Atomicity
### 
Learning Databases? Don’t Overlook ACID Principles. Atomicity
Learn How Atomicity Prevents Data Corruption and Ensures Transaction Reliability
Sergey Egorenkov
Feb 1
Learning Databases? Don’t Overlook ACID Principles. Durability
### 
Learning Databases? Don’t Overlook ACID Principles. Durability
Discover how systems ensure database durability, balancing speed, reliability, and crash recovery through efficient change logging.
Sergey Egorenkov
Jan 31
Learning Databases? Don’t Overlook ACID Principles. Consistency
### 
Learning Databases? Don’t Overlook ACID Principles. Consistency
Learn why consistency in databases matters, its role in ACID, and how to keep your data reliable.
Sergey Egorenkov
Jan 28
Learning Databases? Don’t Overlook ACID Principles. Isolation
### 
Learning Databases? Don’t Overlook ACID Principles. Isolation
Mastering the Key to Consistent and Reliable Transactions
Sergey Egorenkov
Jan 26
About DatabasesLatest StoriesArchiveAbout MediumTermsPrivacyTeams


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com/databases-in-simple-words%3F~feature=LoMobileNavBar&~channel=ShowCollectionHome&~stage=m2
- https://twitter.com/egorenkovserg
Homepage
Open in app
Sign inGet started
# DATABASES
Follow
Why NoSQL Was Invented (and Where SQL Failed Us)
### 
Why NoSQL Was Invented (and Where SQL Failed Us)
Exploring the architectural trade-offs that led to the rise of NoSQL systems.
Sergey Egorenkov
May 3
MVCC in Databases: How It Works and Why It’s Needed
### 
MVCC in Databases: How It Works and Why It’s Needed
Why modern databases use MVCC and what it costs.
Sergey Egorenkov
Apr 22
UUID vs Auto-Increment Integer for IDs. What you should choose
### 
UUID vs Auto-Increment Integer for IDs. What you should choose
Make the right decision when designing your database schema
Sergey Egorenkov
Apr 1
Why Uber Moved from Postgres to MySQL
### 
Why Uber Moved from Postgres to MySQL
How PostgreSQL’s architecture clashed with Uber’s scale — and why MySQL offered a better path forward
Sergey Egorenkov
Mar 28
Database Partitioning Disadvantages You Should Know
### 
Database Partitioning Disadvantages You Should Know
Partitioning Can Cause Problems — Understand Them Before Implementation
Sergey Egorenkov
Mar 21
Making SQL query 40x faster for 10 million rows table
### 
Making SQL query 40x faster for 10 million rows table
Make your SQL query really fast using this approach
Sergey Egorenkov
Mar 17
How to get complete analysis of your SQL query and how to read it
### 
How to get complete analysis of your SQL query and how to read it
Know more about your SQL queries and adjust your approach accordingly
Sergey Egorenkov
Mar 15
Row vs Column-Oriented Databases
### 
Row vs Column-Oriented Databases
Understanding the Key Differences, Strengths, and Use Cases of Row and Column-Oriented Databases
Sergey Egorenkov
Mar 12
How Database Indexes Work (In Simple Words)
### 
How Database Indexes Work (In Simple Words)
Learn how indexing is working and make your database queries much faster.
Sergey Egorenkov
Mar 1
4 Foundational Principles of Databases. ACID
### 
4 Foundational Principles of Databases. ACID
The Backbone of Reliable Transactions: Ensuring Integrity with ACID Principles
Sergey Egorenkov
Feb 18
Breaking Down the Anatomy of a Database Page
### 
Breaking Down the Anatomy of a Database Page
Database Page Structures: How Data is Organized and Retrieved
Sergey Egorenkov
Feb 7
The N+1 Database Query Problem: A Simple Explanation and Solutions
### 
The N+1 Database Query Problem: A Simple Explanation and Solutions
Understanding the N+1 Query Problem: How to Optimize Database Performance and Avoid Slow Queries
Sergey Egorenkov
Feb 5
Learning Databases? Don’t Overlook ACID Principles. Atomicity
### 
Learning Databases? Don’t Overlook ACID Principles. Atomicity
Learn How Atomicity Prevents Data Corruption and Ensures Transaction Reliability
Sergey Egorenkov
Feb 1
Learning Databases? Don’t Overlook ACID Principles. Durability
### 
Learning Databases? Don’t Overlook ACID Principles. Durability
Discover how systems ensure database durability, balancing speed, reliability, and crash recovery through efficient change logging.
Sergey Egorenkov
Jan 31
Learning Databases? Don’t Overlook ACID Principles. Consistency
### 
Learning Databases? Don’t Overlook ACID Principles. Consistency
Learn why consistency in databases matters, its role in ACID, and how to keep your data reliable.
Sergey Egorenkov
Jan 28
Learning Databases? Don’t Overlook ACID Principles. Isolation
### 
Learning Databases? Don’t Overlook ACID Principles. Isolation
Mastering the Key to Consistent and Reliable Transactions
Sergey Egorenkov
Jan 26
About DatabasesLatest StoriesArchiveAbout MediumTermsPrivacyTeams


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com/databases-in-simple-words%3F~feature=LoMobileNavBar&~channel=ShowCollectionHome&~stage=m2
- https://twitter.com/egorenkovserg
Homepage
Open in app
Sign inGet started
# DATABASES
Follow
Why NoSQL Was Invented (and Where SQL Failed Us)
### 
Why NoSQL Was Invented (and Where SQL Failed Us)
Exploring the architectural trade-offs that led to the rise of NoSQL systems.
Sergey Egorenkov
May 3
MVCC in Databases: How It Works and Why It’s Needed
### 
MVCC in Databases: How It Works and Why It’s Needed
Why modern databases use MVCC and what it costs.
Sergey Egorenkov
Apr 22
UUID vs Auto-Increment Integer for IDs. What you should choose
### 
UUID vs Auto-Increment Integer for IDs. What you should choose
Make the right decision when designing your database schema
Sergey Egorenkov
Apr 1
Why Uber Moved from Postgres to MySQL
### 
Why Uber Moved from Postgres to MySQL
How PostgreSQL’s architecture clashed with Uber’s scale — and why MySQL offered a better path forward
Sergey Egorenkov
Mar 28
Database Partitioning Disadvantages You Should Know
### 
Database Partitioning Disadvantages You Should Know
Partitioning Can Cause Problems — Understand Them Before Implementation
Sergey Egorenkov
Mar 21
Making SQL query 40x faster for 10 million rows table
### 
Making SQL query 40x faster for 10 million rows table
Make your SQL query really fast using this approach
Sergey Egorenkov
Mar 17
How to get complete analysis of your SQL query and how to read it
### 
How to get complete analysis of your SQL query and how to read it
Know more about your SQL queries and adjust your approach accordingly
Sergey Egorenkov
Mar 15
Row vs Column-Oriented Databases
### 
Row vs Column-Oriented Databases
Understanding the Key Differences, Strengths, and Use Cases of Row and Column-Oriented Databases
Sergey Egorenkov
Mar 12
How Database Indexes Work (In Simple Words)
### 
How Database Indexes Work (In Simple Words)
Learn how indexing is working and make your database queries much faster.
Sergey Egorenkov
Mar 1
4 Foundational Principles of Databases. ACID
### 
4 Foundational Principles of Databases. ACID
The Backbone of Reliable Transactions: Ensuring Integrity with ACID Principles
Sergey Egorenkov
Feb 18
Breaking Down the Anatomy of a Database Page
### 
Breaking Down the Anatomy of a Database Page
Database Page Structures: How Data is Organized and Retrieved
Sergey Egorenkov
Feb 7
The N+1 Database Query Problem: A Simple Explanation and Solutions
### 
The N+1 Database Query Problem: A Simple Explanation and Solutions
Understanding the N+1 Query Problem: How to Optimize Database Performance and Avoid Slow Queries
Sergey Egorenkov
Feb 5
Learning Databases? Don’t Overlook ACID Principles. Atomicity
### 
Learning Databases? Don’t Overlook ACID Principles. Atomicity
Learn How Atomicity Prevents Data Corruption and Ensures Transaction Reliability
Sergey Egorenkov
Feb 1
Learning Databases? Don’t Overlook ACID Principles. Durability
### 
Learning Databases? Don’t Overlook ACID Principles. Durability
Discover how systems ensure database durability, balancing speed, reliability, and crash recovery through efficient change logging.
Sergey Egorenkov
Jan 31
Learning Databases? Don’t Overlook ACID Principles. Consistency
### 
Learning Databases? Don’t Overlook ACID Principles. Consistency
Learn why consistency in databases matters, its role in ACID, and how to keep your data reliable.
Sergey Egorenkov
Jan 28
Learning Databases? Don’t Overlook ACID Principles. Isolation
### 
Learning Databases? Don’t Overlook ACID Principles. Isolation
Mastering the Key to Consistent and Reliable Transactions
Sergey Egorenkov
Jan 26
About DatabasesLatest StoriesArchiveAbout MediumTermsPrivacyTeams


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com/databases-in-simple-words%3F~feature=LoMobileNavBar&~channel=ShowCollectionHome&~stage=m2
- https://twitter.com/egorenkovserg
Sitemap
Open in app
Sign up
Sign in
Medium Logo
Write
Sign up
Sign in
## 
Databases
·
Follow publication
“Databases” is a publication dedicated to deepening your understanding of databases. From ACID principles to performance tuning, indexing and query optimization, we break down database concepts in a simple, practical way.
Follow publication
Member-only story
# **Why NoSQL Was Invented (and Where SQL Failed Us)**
Sergey Egorenkov
Follow
11 min read
·
May 3, 2025
3
1
Listen
Share
# **Part 1. The Era of SQL and Its Strengths**
Before we talk about why SQL stopped being the only choice, let’s discuss why it was the go-to tool in the first place — and how it earned that spot.
## The Reign of Relational Databases
In the beginning, there was Oracle. And IBM DB2. And eventually MySQL and PostgreSQL. Relational databases were everywhere. Because they solved the problems developers had in the ’80s, ’90s, and early 2000s:
  * Storing structured data.
  * Making sure data relationships stayed consistent.
  * Performing complex queries — and doing it all reliably.


Everything in SQL land was about structure. Tables with fixed schemas, relationships enforced by foreign keys, and guarantees that your data wasn’t going to end up in some weird half-saved state. That structure made things safe and predictable, and in business systems, that’s gold.
In fact, relational algebra (the math behind SQL) gave the whole model a solid theoretical foundation. It wasn’t just a bunch of hacks that happened to work. It was based on decades of database theory.
## ACID Transactions: The Gold Standard of Consistency
## 
Create an account to read the full story.
The author made this story available to Medium members only.  
If you’re new to Medium, create a new account to read this story on us.
Continue in app
Or, continue in mobile web
Already have an account? Sign in
3
3
1
Follow
## Published in Databases
351 followers
·Last published May 3, 2025
“Databases” is a publication dedicated to deepening your understanding of databases. From ACID principles to performance tuning, indexing and query optimization, we break down database concepts in a simple, practical way.
Follow
Follow
## Written by Sergey Egorenkov
376 followers
·31 following
Senior Software Engineer. Writing about software development with deep insights & real-world experience. You can reach out to me via email: egsesmail@gmail.com.
Follow
## Responses (1)
Write a response
What are your thoughts?
Cancel
Respond
Khun Yee Fung, Ph.D.
May 10
Today, it’s about using the right tool for the job
```

Isn't this always the case, not just today?

```

1 reply
Reply
## More from Sergey Egorenkov and Databases
In
Databases
by
Sergey Egorenkov
## Why Uber Moved from Postgres to MySQL
### How PostgreSQL’s architecture clashed with Uber’s scale — and why MySQL offered a better path forward
Mar 29
A clap icon1.5K
A response icon37
In
Databases
by
Sergey Egorenkov
## The N+1 Database Query Problem: A Simple Explanation and Solutions
### Understanding the N+1 Query Problem: How to Optimize Database Performance and Avoid Slow Queries
Feb 6
A clap icon5
In
Databases
by
Sergey Egorenkov
## UUID vs Auto-Increment Integer for IDs. What you should choose
### Make the right decision when designing your database schema
Apr 2
A clap icon26
A response icon4
In
Toxic Engineering
by
Sergey Egorenkov
## Worst Node.js Practices to Use If You Want to Destroy Your App
### A guide to build a Node.js app engineered to destroy performance, security, and maintainability.
Apr 11
A clap icon25
A response icon3
See all from Sergey Egorenkov
See all from Databases
## Recommended from Medium
The Latency Gambler
## We Cut 80% of Our Query Time by Using This Little-Known SQL Pattern
### A simple CTE trick that saved us from a major scaling disaster
May 5
A clap icon1.2K
A response icon26
In
Level Up Coding
by
Varsha Das
## 37 Lessons From My 7 Years in Software Engineering
### These You Will Never Find in Degrees or Tutorials
Jun 9
A clap icon982
A response icon34
In
Psychology of Workplaces
by
George J. Ziogas
## Resumes Are Dying — Here’s What’s Replacing Them
### How modern hiring is leaving resumes behind
Jun 8
A clap icon13.4K
A response icon379
Syarif
## The Illusion of Simplicity: What We Learned from Our Microservice Architecture
Jun 4
A clap icon89
A response icon2
In
AI & Analytics Diaries
by
Analyst Uttam
## Cut Database Costs by 60% Using These 10 SQL Tricks
### How to keep your database bills low while making your queries fly like a sports car
May 27
A clap icon222
A response icon5
Sohail Saifi
## Kubernetes Is Dead: Why Tech Giants Are Secretly Moving to These 5 Orchestration Alternatives
### I still remember that strange silence in the meeting room. Our CTO had just announced we were moving away from Kubernetes after two years…
Jun 7
A clap icon2.2K
A response icon87
See more recommendations
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2Fp%2Fc52929408682&%7Efeature=LoOpenInAppButton&%7Echannel=ShowPostUnderCollection&%7Estage=mobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2Fp%2Fc52929408682&%7Efeature=LoOpenInAppButton&%7Echannel=ShowPostUnderCollection&%7Estage=regwall&source=-----c52929408682---------------------post_regwall------------------
- egsesmail@gmail.com
- https://medium.statuspage.io/?source=post_page-----c52929408682---------------------------------------
- pressinquiries@medium.com
- https://speechify.com/medium?source=post_page-----c52929408682---------------------------------------
Sitemap
Open in app
Sign up
Sign in
Medium Logo
Write
Sign up
Sign in
Sergey Egorenkov
376 followers
Follow
Home
About
Published in
DevOps and Architecture
## Costs of Microservices You Should Know Before Breaking Up Your Monolith
### A practical look at the hidden trade-offs behind microservice architectures.
Jun 2
A clap icon59
Jun 2
A clap icon59
Published in
DevOps and Architecture
## Microservices Data Flow: Sync, Async, and Async That Scales
### So you’re building a content platform. Think Medium or Substack — users can publish articles, others can follow, like, comment, share…
May 28
A clap icon13
May 28
A clap icon13
Published in
CyberSecurity
## AI Can Hack Your App in Seconds. Here Is What You Can Do
### How AI is accelerating attacks — and what developers can do to defend their apps.
May 8
A clap icon4
May 8
A clap icon4
Published in
Databases
## Why NoSQL Was Invented (and Where SQL Failed Us)
### Exploring the architectural trade-offs that led to the rise of NoSQL systems.
May 3
A clap icon3
A response icon1
May 3
A clap icon3
A response icon1
Published in
CyberSecurity
## Refresh Tokens Are Trickier Than Many Developers Think
### It’s not enough to make them work, here’s how to make them secure, reliable, and hard to exploit.
Apr 30
A clap icon3
Apr 30
A clap icon3
Published in
CyberSecurity
## Why JWT Needs a Secret If It’s Not Encrypted
### This comes up more often than you’d expect…
Apr 30
A clap icon3
Apr 30
A clap icon3
Published in
Databases
## MVCC in Databases: How It Works and Why It’s Needed
### Why modern databases use MVCC and what it costs.
Apr 22
A clap icon39
A response icon1
Apr 22
A clap icon39
A response icon1
Published in
Toxic Engineering
## The Nonsense of JavaScript
### You should be ready for this when writing JavaScript.
Apr 12
A clap icon7
A response icon3
Apr 12
A clap icon7
A response icon3
Published in
Toxic Engineering
## Worst Node.js Practices to Use If You Want to Destroy Your App
### A guide to build a Node.js app engineered to destroy performance, security, and maintainability.
Apr 11
A clap icon25
A response icon3
Apr 11
A clap icon25
A response icon3
Published in
Toxic Engineering
## TypeScript: The Ball and Chain You Begged For
### A brutally honest look at the cost of TypeScript.
Apr 5
A clap icon9
A response icon1
Apr 5
A clap icon9
A response icon1
## Sergey Egorenkov
376 followers
Senior Software Engineer. Writing about software development with deep insights & real-world experience. You can reach out to me via email: egsesmail@gmail.com.
Follow
Following
  * DevOps and Architecture
  * CyberSecurity
  * Tac Tacelosky
  * Kevin Masur
  * XeusNguyen


See all (31)
Help
Status
About
Careers
Press
Blog
Privacy
Rules
Terms
Text to speech


# Liens externes trouvés
- https://rsci.app.link/?%24canonical_url=https%3A%2F%2Fmedium.com%2F%40egorenkovserg&%7Efeature=LoOpenInAppButton&%7Echannel=ShowUser&%7Estage=mobileNavBar&source=---two_column_layout_nav-----------------------------------------
- egsesmail@gmail.com
- https://medium.statuspage.io/?source=user_profile_page---user_sidebar-------------------2ad674831bd----------------------
- pressinquiries@medium.com
- https://speechify.com/medium?source=user_profile_page---user_sidebar-------------------2ad674831bd----------------------
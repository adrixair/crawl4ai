⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Blog|Tutorials
Table of contents «Close »
#### Table of contents
  * What is the N+1 query problem?
  * An example N+1 query
  * What caused the N+1 query problem?
  * Creating data structures for more complicated queries
  * Identifying N+1 queries
    * PlanetScale Insights


Want to learn more about unlimited IOPS w/ Metal, Vitess, horizontal sharding, or Enterprise options?
Talk to Solutions
Get the RSS feed
# What is the N+1 Query Problem and How to Solve it?
By JD Lien | January 18, 2023
Have you ever been working on an app, staring at your screen waiting for it to load, wondering what on Earth is going on? There are a lot of reasons why you could be experiencing performance issues, but a classic cause of performance issues in database-driven applications is the dreaded **N+1 query problem**.
Tip
If you're wondering if you have an N+1 problem, you can sign up for a PlanetScale account to access our Insights query monitoring dashboard. More information about identifying N+1s with Insights at the end of this article. 
## What is the N+1 query problem?
The chief symptom of this problem is that there are many, many queries being performed. Typically, this happens when you structure your code so that you first do a query to get a list of records, then subsequently do another query for each of those records.
You might expect that many small queries would be fast and one large, complex query will be slow. This is rarely the case. In practice, the opposite is true. Each query has to be sent to the database, the database has to perform the query, then it sends the results back to your app. The more queries you perform, the more time it takes to get the results back, with each trip to the database server taking time and resources. In contrast, a single query, even if it's complex, can be optimized by the database server and only requires one trip to the database, which will usually be much faster than many small queries.
## An example N+1 query
Tip
As you read through these examples, you can view a live demo here detailing the results and query run time. 
Let's look at an example. Applications typically query several related records from the same database tables. Let's take an example of grocery items and categories from my previous article on joins. In this example scenario, we have a PlanetScale database with an `items` table and a `categories` table. The `items` table contains a list of grocery store items with their corresponding categories in the `categories` table. The examples are in PHP, but the same principles apply to any language.
**`categories`table:**
id name  
1 Produce  
2 Deli  
3 Dairy  
**`items`table:**
id name category_id  
1 Apples 1  
2 Cheese 2  
3 Bread NULL  
Let's say we want our application to list all of the items, including the _name_ of the category they belong to. One straightforward way we could do this is by first querying a list of categories, and then looping over each of the categories, querying for each category's items.
**First query — Grabbing the categories:**
```
<?php
    $dbh = new Dbh();
    $conn = $dbh->connect();
    $sql = "SELECT * FROM categories;";
    $stmt = $conn->prepare($sql);
    $stmt->execute();

```

**Second query — Looping over each category and grabbing the items:**
```
<?php
while ($row = $stmt->fetch()) {
    // Show category name
    echo $row['name'];

    // Now query for the items for this category
    $sql = "
        SELECT id, name FROM items
        WHERE category_id = :category_id
        ORDER BY name;
    ";

    $stmt2 = $conn->prepare($sql);
    $stmt2->bindParam(':category_id', $row['id']);
    $stmt2->execute();
    $rowCount += $stmt2->rowCount();

    while ($row2 = $stmt2->fetch()) {
        // Show item ID and name
        echo $row2['id'];
        echo $row2['name'];
    }
}

```

This approach has the benefits of having two simple queries and clear, procedural code. Unfortunately, this approach is flawed, and you should avoid this situation where you are executing many database queries in a loop.
## What caused the N+1 query problem?
This type of query execution is often called "N+1 queries" because instead of doing the work in a single query, you are running one query to get the list of categories, then another query for every _N_ categories. Hence the term "_N_ +1 queries".
You can find the demo of the results being ran here: Demo — N+1 queries to get categories and items
In the above example, our database contains about 800 items across 17 categories. It takes over 1 second to run the 18 simple queries involved in this! That's pretty slow. If you have a more complex queries with a lot of data, it will take even longer.
For this simple example, it's possible to perform the exact same job 10× faster by using only **one** query that uses a `JOIN` clause. We could refactor the above code to look something like this:
```
<?php
    $dbh = new Dbh();
    $conn = $dbh->connect();
    // Record the time before the query is executed
    $timeStart = microtime(true);

    $sql = "
        SELECT
            c.id AS category_id,
            c.name AS category_name,
            i.id AS item_id,
            i.name AS item_name
        FROM categories c
        LEFT JOIN items i ON c.id = i.category_id
        ORDER BY c.name, i.name;
    ";
    $stmt = $conn->prepare($sql);

    $stmt->execute();
    $rowCount = $stmt->rowCount();

    $lastCategoryId = null;

    while ($row = $stmt->fetch()) {
        // Render the heading for each category if this category is new
        if ($row['category_id'] != $lastCategoryId) {
            echo $row['category_name'];
        }

        // Display the row for each item
        if (!is_null($row['item_id'])) {
            echo $row['item_id'];
            echo $row['item_name'];
        }

        $lastCategoryId = $row['category_id'];
    }

```

With this update, we accomplished much the same work with a single, slightly more complicated query. Attempting our demo of this again, we can observe a significant performance difference between the original page and this one! The page loads in about 0.16 seconds, instead of 1.4 seconds.
  * Demo app — Categories with Items (n+1) Queries
  * Categories — with Items (Single Query)


In this simple example, with a database that isn't very large, the _n_ +1 approach takes about **10 times longer!**
Imagine you had thousands, or **millions** of records. The performance delta could be the difference between a reasonable load time and a page that takes so long to load that it causes a timeout on the server.
## Creating data structures for more complicated queries
Sometimes you may have a more complicated operation in mind. Say you wanted to show the categories along with the count of each item in each category. You _could_ use an aggregate query (`GROUP BY`), as shown below:
```
SELECT c.id, c.name, count(i.id) AS item_count FROM categories c
LEFT JOIN items i ON c.id = i.category_id
GROUP BY c.id, c.name
ORDER BY c.name;

```

But then how would we also get the list of items from a query like this where we are grouping?
While it's often most efficient to let the database server do a lot of the heavy lifting instead of our server-side code, for something like a simple count of items, it may not be necessary. If we actually just queried for the items, it's pretty easy to let the server-side code (PHP, in our example) do the count for us!
We can refactor this such that we do the job with a single query, then turn that query into a clean data structure.
```
<?php
$dbh = new Dbh();
$conn = $dbh->connect();
// Record the time before the query is executed
$timeStart = microtime(true);

$sql = "
    SELECT
        c.id AS category_id,
        c.name AS category_name,
        i.id AS item_id,
        i.name AS item_name
    FROM categories c
    -- Using a normal JOIN would not get the categories with 0 items
    LEFT JOIN items i ON c.id = i.category_id
    ORDER BY c.name, i.name;
";
$stmt = $conn->prepare($sql);

$stmt->execute();
$rowCount = $stmt->rowCount();

$lastCategoryId = null;
$lastCategoryName = null;

// Build a 2D array of categories with their items
$categories = [];
// A categoryItems array will become the value for each category
$categoryItems = [];

// Alternative approach: build a data structure with the data we want as a 2D array.
while ($row = $stmt->fetch()) {
    // Render the heading for each category if this category is new
    if (!is_null($lastCategoryId) && $row['category_id'] != $lastCategoryId) {
        $categories[$lastCategoryName] = $categoryItems;
        // Reset the categoryItems array
        $categoryItems = array();
    }

    // Create an array of all the non-null items
    if (!is_null($row['item_id'])) $categoryItems[$row['item_id']] = $row['item_name'];

    $lastCategoryId = $row['category_id'];
    $lastCategoryName = $row['category_name'];
}
// Add the last category to the array with its items
$categories[$lastCategoryName] = $categoryItems;

```

Now that we have this `$categories` array with arrays of items within, we can do a nested loop to render the data in the way we see fit. When we want the count of items, you can simply run `count($items)` to get the quantity.
```
<?php
foreach ($categories as $categoryName => $items) {
    echo $categoryName;
    // Show the count of items in the category
    echo count($items) . ' items';

    if (count($items)) {
        // Loop through all the items in the category and display them
        foreach($items as $itemId => $itemName) {
            echo $itemId;
            echo $itemName;
        }
    }

```

Using techniques like this, you can keep your page load times quite fast by being efficient with your use of the database. Instead of writing your code such that you have 1 query plus another for each record of that query, it is well-worth the effort to write your code such that you have 1 query that returns all the data you need.
Using this approach, you can also create data structures that are more useful for your application. For example, you may want to create a data structure that is keyed by the category ID, and then have the items as sub-arrays. This would allow you to easily access the items for a specific category by its ID.
## Identifying N+1 queries
If you have a more complex application, you may have a lot of N+1 queries and not know it. There are a few ways to identify these queries and fix them.
If you're working on a Laravel app you can use Laravel Debug Bar. Laravel also allows you to fully disable N+1 queries by adding the following line to your `AppServiceProvider` inside the `boot` method:
```
Model::preventLazyLoading(!app()->isProduction());

```

This will cause the application to throw an exception if it detects an N+1 query when not in production, allowing you to detect and fix these issues.
### PlanetScale Insights
PlanetScale also offers an analytics and monitoring solution called PlanetScale Insights. This is accessible from your PlanetScale dashboard and allows you to see the queries that are being run on your database. Using this, you can identify many types of issues with your queries, including N+1 queries and long-running queries. The screenshot below is from the demo database we've been using in this article.
The first query is our more complex but efficient `JOIN` query, which read 834 rows, returned 815 rows, and took a total of 14ms.
The two queries below that are inefficient queries that resulted in the N+1 problem. Together, they took a total of 42ms and 13,889 rows read to give us the same results as the more complex query.
Overall, this shows us right away that our N+1 queries:
  * Ran way too many times
  * Read way more rows than returned
  * And performance was relatively slow


Now you know how to identify N+1 queries, how to fix them, and how to use PlanetScale Insights to monitor your queries and identify performance issues so you can get out there and write some fast, lean code!
## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://n-plus-1.planetscale.vercel.app
- https://n-plus-1.planetscale.vercel.app/categories-with-items.php
- https://n-plus-1.planetscale.vercel.app/categories-with-items-single-query.php
- https://github.com/barryvdh/laravel-debugbar
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


# The world’s fastest and most reliable relational database
The PlanetScale platform delivers horizontal scale, incredible performance, and simplified operations — no matter the size of your business. Backed by Vitess, PlanetScale makes achieving a shared-nothing architecture with explicit sharding simpler than ever.
Our blazing fast NVMe drives unlock **unlimited IOPS** , bringing data center performance to the cloud. We offer a range of deployment options to cover all of your security and compliance requirements — including bring your own cloud with PlanetScale Managed.
  * Performance
  * Vitess
  * Uptime


  * Cost
  * Security
  * Features


Our technology powers Tier 0 databases at:
Read case studyRead case studyRead case studyRead case study
> When you buy PlanetScale, you’re getting the technology and database expertise that ran and scaled YouTube, the internet’s #2 site, and the team that scaled GitHub to over 100M users globally.
– Todd Berman @Attentive
* * *
## Performance
PlanetScale Metal allows you to run your database on the fastest servers available in the cloud. Our blazing fast NVMe drives unlock unlimited IOPS and drastically lower latencies compared to other cloud database providers like Amazon Aurora and GCP Cloud SQL.
The graph above displays the p50, p95, and p99 change after moving a database to Metal. See more benchmarks on our Benchmarking page.  

> We are very happy with our decision to migrate to PlanetScale Metal which enabled us to achieve the rare outcome of improvements in performance, cost, and reliability – a win for our customers and our business.
– Aaron Young @ Cash App
## Vitess
Vitess allows MySQL databases to scale horizontally through explicit sharding — enabling a shared nothing architecture distributing data across thousands of nodes, all routed through a single database connection.
Vitess was developed at YouTube by the founders of PlanetScale to scale their main MySQL database to petabytes of data on 70,000 nodes across 20 data centers. Now maintained and managed by PlanetScale, Vitess powers the databases of some of the web’s largest properties: Slack, HubSpot, Blizzard, Etsy, GitHub, Block, Bloomberg, Yelp, and more.
```

   ┌────────────────────────────────┐   
   │░░░░░░░░░░░░░VTGate░░░░░░░░░░░░░│   
   └────────────────────────────────┘   
                    │                   
                                        
          ─ ─ ─ ─ ─ ┴ ─ ─ ─ ─ ┐         
         │                              
                              │         
         ▼                    ▼         
   ╔═══════════╗        ╔═══════════╗   
   ║           ║        ║           ║   
   ║  Primary  ║        ║  Primary  ║   
   ║           ║        ║           ║   
   ╚═══════════╝        ╚═══════════╝   
         │                    │         
                                        
     ─ ─ ┴ ─ ─            ─ ─ ┴ ─ ─     
    │         │          │         │    
    ▼         ▼          ▼         ▼    
┌───────┐ ┌───────┐  ┌───────┐ ┌───────┐
│Replica│ │Replica│  │Replica│ │Replica│
└───────┘ └───────┘  └───────┘ └───────┘

```
```

           ┌──────────────────────────────────┐            
           │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│            
           │░░░░░░░░░░░░░░VTGate░░░░░░░░░░░░░░│            
           │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│            
           └──────────────────────────────────┘            
                             │                             
                                                           
         ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┼ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐         
                                                           
         │                   │                   │         
         ▼                   ▼                   ▼         
   ╔═══════════╗       ╔═══════════╗       ╔═══════════╗   
   ║           ║       ║           ║       ║           ║   
   ║  Primary  ║       ║  Primary  ║       ║  Primary  ║   
   ║           ║       ║           ║       ║           ║   
   ╚═══════════╝       ╚═══════════╝       ╚═══════════╝   
         │                   │                   │         
                                                           
     ─ ─ ┴ ─ ─           ─ ─ ┴ ─ ─           ─ ─ ┴ ─ ─     
    │         │         │         │         │         │    
    ▼         ▼         ▼         ▼         ▼         ▼    
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Replica│ │Replica│ │Replica│ │Replica│ │Replica│ │Replica│
└───────┘ └───────┘ └───────┘ └───────┘ └───────┘ └───────┘

```
```

               ┌─────────────────────────────────────────────────────────┐               
               │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│               
               │░░░░░░░░░░░░░░░░░░░░░░░░░VTGate░░░░░░░░░░░░░░░░░░░░░░░░░░│               
               │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│               
               └─────────────────────────────────────────────────────────┘               
                                            │                                            
                                                                                         
              ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┼ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─              
             │                                                             │             
             ▼                              ▼                              ▼             
   ╔═══════════════════╗          ╔═══════════════════╗          ╔═══════════════════╗   
   ║                   ║          ║                   ║          ║                   ║   
   ║                   ║          ║                   ║          ║                   ║   
   ║      Primary      ║          ║      Primary      ║          ║      Primary      ║   
   ║                   ║          ║                   ║          ║                   ║   
   ║                   ║          ║                   ║          ║                   ║   
   ╚═══════════════════╝          ╚═══════════════════╝          ╚═══════════════════╝   
             │                              │                              │             
      ┌ ─ ─ ─ ─ ─ ─ ┐                ┌ ─ ─ ─ ─ ─ ─ ┐                ┌ ─ ─ ─ ─ ─ ─ ┐      
      ▼             ▼                ▼             ▼                ▼             ▼      
┌───────────┐ ┌───────────┐    ┌───────────┐ ┌───────────┐    ┌───────────┐ ┌───────────┐
│           │ │           │    │           │ │           │    │           │ │           │
│  Replica  │ │  Replica  │    │  Replica  │ │  Replica  │    │  Replica  │ │  Replica  │
│           │ │           │    │           │ │           │    │           │ │           │
└───────────┘ └───────────┘    └───────────┘ └───────────┘    └───────────┘ └───────────┘

```

> Our migration to Vitess is more than just a technological upgrade; it’s a strategic move to future-proof our database architecture for the next decade and beyond.
– Ryan Sherlock @Intercom
* * *
## Uptime
Ensuring your database is always running and your data is always safe is our number one priority. Nothing comes before uptime and reliability. Our SLA commitment is 99.999% for multi-region deployments and 99.99% for single-region deployments.
PlanetScale’s platform far exceeds the reliability of database services like Amazon Aurora/RDS and Google Cloud SQL with superior architecture and by making all database operations online.
  * Deploy schema changes fully online
  * Revertable schema changes (with zero data loss)
  * Directing traffic to new read-only replicas
  * Online MySQL and Vitess version updates
  * Online cluster resizing and resharding


You can check out our track record on our status page.
* * *
## Cost
At PlanetScale we believe cost is a unit of scale. Our product is less expensive than RDS MySQL and Aurora for around 85% of the workloads that customers have migrated to Metal. Getting a custom quote is easy: reach out to us. No long sales process or annoying pitches — you can probably tell from our website that the tech speaks for itself.
  * No matter the size of your workload, PlanetScale Metal has the best price to performance ratio of any database service.
  * Bring your own cloud and commitment discounts with PlanetScale Managed
  * Purchase through the AWS Marketplace or the GCP Marketplace
  * Customers running Metal on PlanetScale Managed can realize additional savings through Reserved Instances or Savings Plans — discounts otherwise not available on traditional EBS volumes.


* * *
## Security
PlanetScale is trusted by some of the world’s largest brands. Our core infrastructure was built to comply with high standards of security, compliance, and privacy.
  * SOC 2 Type 2+ HIPAA compliance
  * PCI DSS 4.0 compliance as a Level 1 Service Provider
  * HIPAA Business Associate Agreements available on all plans


Learn more about our security and compliance practices in the security documentation.
> We have very strict regulatory requirements that can feel painful to the average engineer, however PlanetScale was a strong partner in grinding through our asks, leaving us in a place where everyone was happy.
– Aaron Young @Cash App
Visit our Trust Center to request the latest copy of our SOC 2 Type 2 report, PCI DSS Attestation of Compliance, and more.
* * *
## Features
PlanetScale is an opinionated database platform built by the infrastructure teams behind Facebook, GitHub, Twitter, Slack, YouTube, and more. All of our features combine to provide an end-to-end database management platform that prevents human error and provides full insight into query performance with actionable recommendations to make your database faster.
  * Branching and deploy requests for zero downtime schema changes that your team can review.
  * Store your vector data alongside your application’s relational MySQL data with PlanetScale vector support.
  * Roll back bad schema changes with no downtime and no data loss.
  * Full database observability with Insights to give you a detailed overview of cluster health.
  * Automate the horizontal scaling of your database with our explicit sharding workflows.
  * Utilize our Global Edge Network to automatically route query traffic to local nodes.
  * Integrations with Fivetran, Airbyte, Hightouch, Datadog, Vantage, Debezium, and more.
  * All of this is backed by our best-in-class support.


> Databases are hard. We would rather PlanetScale manage them. We wanted the support PlanetScale offers because they are the experts in the field. We’ve seen this come to fruition in our relationship.
– Chris Karper @ MyFitnessPal
## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://pscale.link/int
- https://www.planetscalestatus.com/
- https://aws.amazon.com/marketplace/pp/prodview-luy3krhkpjne4
- https://console.cloud.google.com/marketplace/product/planetscale-public/planetscale-database
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
## Sign in
New to PlanetScale? Sign up for an account. 
Email
Password
show 
Forgot password?
Sign in
* * *
Or with
Single sign-on

## Sign up
Already have an account? Sign in. 
Email
Password
show 
Password confirmation
show 
By registering, you agree to the processing of your personal data by PlanetScale as described in the Privacy Policy. 
I've read and agree to the Terms of Service
Sign up
* * *
OR

⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


# Features
PlanetScale is a MySQL-compatible database that brings you scale, performance, reliability, and cost-efficiencies — without sacrificing developer experience.
Each PlanetScale feature was designed to solve problems that database, reliability, and product engineering teams commonly face during daily operations.
With built-in online schema changes, you never have to deal with downtime or manually configure solutions like gh-ost or pt-online-schema-change. Deep and actionable query analytics ensure you can quickly debug issues and surface queries that can be improved. These are just a couple examples of the features we have implemented to make PlanetScale the best end-to-end solution for database hosting, scaling, and management.
* * *
  * **Familiar workflows:** Branch schema like you branch your code.
  * **No compromises:** Unlimited scale and high database performance — you don’t have to choose.
  * **Read-only regions:** Support globally distributed applications with read-only regions.
  * **Zero downtime imports:** Get started in minutes. Keep your existing database running while we do the import.


### Unlimited scale and improved database performance
PlanetScale Metal offers local NVMe drives that unlock unlimited IOPS and unbeatable performance. Keep sharding logic out of your application with PlanetScale's underlying Vitess architecture. With PlanetScale sharding, you can split up large tables across several MySQL instances, leading to better performance, faster maintenance tasks like backups, and improved performance.
Learn more about sharding
### Bring the DevOps workflow to the database
Deploy your schema to production with no locking or downtime with non-blocking schema changes. Roll back problematic schema changes instantly without data loss.
Learn more about deploy requests
### Branch your database like you branch your code
Say goodbye to staging environments. PlanetScale’s branching workflow gives your team additional safeguards when making schema changes. Create an isolated branch of your production schema, make your schema changes, get team approvals, and merge the schema into production with no downtime.
Learn more about branching
### Streamline processes to ship faster
We give you the tools to design processes that work best for your teams. Programmatically manage your database with our API, set up custom GitHub Actions, and more.
  * PlanetScale CLI: Manage your database from the command line
  * API reference: Get started with the PlanetScale API


### Query insights to debug and improve performance
Monitor and debug queries directly from the dashboard with Insights. Unlike similar products, Insights provides a detailed look into **all active queries** running against your database. This allows you to identify queries that are running too long, too often, returning too much data, not using indexes appropriately, producing errors, and more.
Learn more about PlanetScale Insights
### Integrate with your preferred tools
PlanetScale is an OLTP database, and is not always the best solution for OLAP workloads. You likely already have your own preferred tools for these jobs. We have integrated support for Airbyte, Fivetran, and more to ensure you're able to use the best tool for the job.
  * PlanetScale Connect: Easily move data for OLAP


Learn more about PlanetScale Connect
### MySQL-native vector search and storage
With PlanetScale vector support, you can store your vector data alongside your application's relational MySQL data — eliminating the need for a separate, specialized vector database.
  * Pre-filtering and post-filtering
  * Full SQL syntax — including JOIN, WHERE, and subqueries
  * ACID compliance
  * SPANN-based algorithm for large-scale workloads


### Auto-route replica traffic
All PlanetScale clusters are made up of, at minimum, one primary and two replicas in the same region spread across three availability zones. With Global Replica credentials, we seamlessly route traffic to the read-only region with the lowest latency, without dropping the connection.
  * Learn more about PlanetScale Global Network
  * Read the replica documentation


## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


# Contact us
Talk to sales
Chat with us to get a demo, learn about Metal, Vitess, PlanetScale Managed, pricing, which plan is best for your team, and more.
Open a support ticket
Troubleshoot a technical issue or payment problem.
First name<sup>*</sup>Last name<sup>*</sup>Work email<sup>*</sup>Company<sup>*</sup>Questions or comments<sup>*</sup>
I would like a product demo
How did you hear about PlanetScale? (optional)
By clicking submit below, you agree to the processing of your personal information by PlanetScale as described in the Privacy Policy.
Submit
## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Documentation »Close «Search…
## Platform
Getting started
  * What is PlanetScale?
  * PlanetScale architecture
  * PlanetScale workflow
  * Step-by-step guide
  * Cluster sizing
  * Cluster configuration
  * Selecting a region
  * Replicas
  * Foreign key constraints support
  * Web console
  * Terminology
  * MySQL compatibility


Imports
## Database import tool 
  * Database imports
  * Import tool public IP addresses
  * Import tool user permissions


## MySQL to PlanetScale migration 
  * Amazon Aurora
  * Amazon RDS
  * Azure
  * DigitalOcean
  * GCP Cloud SQL
  * MariaDB


## Postgres to PlanetScale migration
  * Postgres overview
  * Postgres directly to PlanetScale
  * Postgres to PlanetScale with intermediate MySQL


Connecting
  * Connect any app
  * Connect a MySQL GUI
  * Connection strings
  * Network latency
  * Model Context Protocol (MCP)

Private connections
  * AWS PrivateLink
  * GCP Private Service Connect


Schema changes
  * Non-blocking schema changes
  * Safe migrations


## Branching 
  * Using branches
  * Data Branching®


## Deploy requests 
  * Using deploy requests
  * Throttling deploy requests
  * Aggressive cutover


## Schema changes 
  * How to make different types of schema changes
  * Automating with GitHub Actions
  * Handling table and column renames
  * Changing primary and unique keys


Monitoring
## PlanetScale Insights 
  * Query Insights
  * Anomalies
  * Schema recommendations


## Prometheus 
  * Connecting Prometheus
  * Visualizing in Grafana
  * Collecting in the Datadog Agent
  * Forwarding metrics to New Relic
  * Metrics List


## Integrations 
  * Datadog (legacy)


## Database auditing 
  * Audit log


Backups
  * Back up and restore


Scaling
  * Cluster sizing
  * Cluster configuration
  * Replicas
  * Read-only regions
  * PlanetScale system limits
  * VTGates


Sharding
## Overview 
  * Sharding with PlanetScale
  * Workflows


## Guides 
  * Sharding quickstart
  * Modifying the number of shards
  * Sharding new tables
  * Avoiding cross-shard queries
  * Keyspace targeting for ORMs and frameworks
  * Creating sequence tables
  * Pre-sharding checklist


## Concepts 
  * VSchema
  * Vindexes
  * Keyspaces
  * Sharding workflow state reference


Vectors
  * Vectors overview
  * Concepts and terminology
  * Use cases
  * Using with an ORM
  * Reference


Metal
  * Metal overview
  * Create a new Metal database
  * Upgrade to Metal
  * Metal plans and sizes
  * Performance on Metal


Security
  * PlanetScale security and compliance overview
  * Vulnerability disclosure


## Database security 
  * Connection strings
  * Secure connections
  * Password roles


## Account access 
  * Authentication methods
  * Multi-factor authentication
  * Account password security
  * Security log


## Organization access 
  * Access control
  * Audit log
  * Teams
  * Single sign-on


Enterprise
  * PlanetScale Managed overview

AWS
  * Overview
  * Set up PlanetScale Managed
  * Set up AWS PrivateLink
  * Set up AWS Reverse PrivateLink
  * Back up and restore
  * Security and access
    * User management
    * Cloud accounts and contents
    * Data requests
    * Schema snapshots


GCP
  * Overview
  * Set up PlanetScale Managed
  * Set up GCP Private Service Connect
  * Back up and restore
  * Security and access
    * User management
    * Cloud accounts and contents
    * Data requests
    * Schema snapshots


## Settings 
  * Maintenance schedules


## Onboarding process 
  * Overview
  * Proof of concept


Troubleshooting
  * MySQL compatibility
  * PlanetScale system limits
  * Errors reference


## Plans and billing
Plans
  * Plans
  * Cluster sizes
  * PlanetScale Managed
  * Deployment options
  * Support plans
  * Database sleeping


Billing
  * Billing
  * Scaler Pro cluster pricing
  * Vantage


## Integrations
Development
  * Cloudflare Workers
  * Netlify
  * Vercel
  * AWS Lambda
  * Automating with GitHub Actions


ETL
  * Overview
  * Airbyte
  * Fivetran
  * Hightouch
  * Stitch
  * Debezium


Monitoring
  * Prometheus
  * Grafana
  * Datadog Agent
  * New Relic
  * Datadog (legacy)


Billing
  * Vantage


## Guides
Frameworks and ORMs
  * Django
  * Golang
    * Go quickstart
    * Gorm
  * Next.js
    * Next.js quickstart
    * Next.js and Netlify template
    * Deploy to Vercel
    * Deploy to Netlify
  * Node.js
  * PHP
    * PHP quickstart
    * Laravel quickstart
    * Symfony quickstart
  * Prisma
    * Prisma quickstart
    * Automatic Prisma migrations
    * Serverless driver with Prisma
    * Prisma best practices
  * Ruby on Rails
    * Ruby on Rails quickstart
    * Automatic Rails migrations


Deployments
  * Deploy to Netlify
  * Deploy to Vercel
  * Next.js and Netlify template
  * Deploy a Django app to Heroku
  * Cloudflare Workers


Monitoring
  * Visualizing in Grafana
  * Sending Prometheus Metrics to Datadog
  * Sending Prometheus Metrics to New Relic


Serverless JavaScript driver
  * Using the serverless driver
  * Node.js example
  * Prisma example


MySQL
  * Operating without foreign key constraints
  * Performing different types of schema changes
  * How online schema change tools work
  * OnlineDDL 
  * Changing unique keys
  * Renaming columns and tables
  * Online schema change tool comparison


## API and CLI
API
  * API and OAuth applications
  * API reference
  * Service tokens


## Webhooks in PlanetScale 
  * Setting up webhooks
  * Webhook events reference


CLI
  * CLI overview


## Using the pscale CLI 
  * Setting up CLI environment
  * Service tokens

CLI command reference
  * api
  * audit-log
  * auth
  * backup
  * branch
  * completion
  * connect
  * database
  * data-imports
  * deploy-request
  * keyspace
  * mcp
  * org
  * password
  * ping
  * region
  * service-token
  * shell
  * signup


# PlanetScale documentation
PlanetScale is a MySQL-compatible database that brings you scale, performance, and reliability — without sacrificing developer experience.
With PlanetScale, you get the power of horizontal sharding, non-blocking schema changes, and many more powerful database features without the pain of implementing them.
### What is PlanetScale?
PlanetScale helps you scale large workloads and speed up development.
Learn more
### PlanetScale quickstart guide
Deploy a database and learn the basics of using PlanetScale with an example.
Learn more
### PlanetScale architecture
Primaries, replicas, load balancers, keyspaces, shards, and more.
Learn more
### Sharding with PlanetScale
Distribute your data across several instances with horizontal sharding.
Learn more
### Branching
Online schema changes with branching and deploy requests.
Learn more
### Import a database
Import a database to PlanetScale with no downtime.
Learn more
## PlanetScale plans
### PlanetScale plans
What's the difference between Scaler Pro and Enterprise?
Learn more
### Deployment options
PlanetScale offers multi-tenant and single-tenant deployment options.
Learn more
### Bring your own cloud
Learn about our Enterprise offering — PlanetScale Managed.
Learn more
« Table of contentsClose »
#### Table of contents
  * PlanetScale plans
    * PlanetScale plans
    * Deployment options
    * Bring your own cloud


## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://docs.netlify.com/integrations/planetscale-integration/
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


# Case studies
Companies worldwide choose PlanetScale to transform their business, starting with their data.
* * *
## Cash App
Cash App's move to PlanetScale resulted in streamlined database operations, improved performance, and reduced operational overhead. →
* * *
## MyFitnessPal
MyFitnessPal chose PlanetScale so they can focus on their data, not the database →
* * *
## Attentive
Attentive can confidently handle a 10× increase in volume on Black Friday/Cyber Monday thanks to PlanetScale. →
* * *
## Barstool Sports
In 15 minutes, Barstool Sports saved millions in outage avoidance →
* * *
## Mintify
Preparing for growth to 30 terabytes with PlanetScale →
* * *
## May
May needed their highly sensitive financial data to stay in France, their infrastructure to stay secure, and the product to stay fast. →
* * *
## Flyclops
Flyclops switched to PlanetScale to handle 100% growth without a DBA →
* * *
## PropFuel
MySQL expertise as an extension of your team →
* * *
## Community
Community chose PlanetScale for flexibility, scale, and speed →
* * *
## WhyDonate
How WhyDonate switched from Google Cloud, saved 80+ work hours, and now pays 8× less →
* * *
## Dub
PlanetScale gives Dub a rock-solid foundation and unmatched development velocity. →
* * *
## Superwall
PlanetScale gives Superwall a scalable platform to handle huge growth trajectory →
## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


# Blog
Get the RSS feed
All|Engineering|Vitess|Product|Tutorials|Company
* * *
## Announcing PlanetScale Metal
[Product]
By Sam Lambert | March 11, 2025
Database goes brrrrrrrrrrr. →
* * *
## Announcing Vitess 22
[Vitess]
By Vitess Engineering Team | April 29, 2025
Vitess 22 is now generally available →
* * *
## PlanetScale vectors is now GA
[Product]
By Patrick Reynolds | March 25, 2025
You can now use vector search and storage in your PlanetScale MySQL database. →
* * *
## Faster interpreters in Go: Catching up with C++
[Engineering]
By Vicent Martí | March 20, 2025
A novel technique for implementing dynamic language interpreters in Go, applied to the Vitess SQL evaluation engine →
* * *
## The Real Failure Rate of EBS
[Engineering]
By Nick Van Wiggeren | March 18, 2025
Our experience running AWS EBS at scale for critical workloads →
* * *
## IO devices and latency
[Engineering]
By Benjamin Dicken | March 13, 2025
Take an interactive journey through the history of IO devices, and learn how IO device latency affects performance. →
* * *
## Upgrading Query Insights to Metal
[Engineering]
By Rafer Hazen | March 11, 2025
Our experience upgrading the Query Insights database to PlanetScale Metal →
* * *
## PlanetScale Metal: There’s no replacement for displacement
[Engineering]
By Richard Crowley | March 11, 2025
Learn how PlanetScale Metal was built and how we ensured it is safe. →
* * *
## Automating cherry-picks between OSS and private forks
[Engineering]
By Manan Gupta | January 14, 2025
Learn how PlanetScale keeps its private fork of Vitess up-to-date with OSS →
* * *
## Database Sharding
[Engineering]
By Benjamin Dicken | January 9, 2025
Learn about the database sharding scaling pattern in this interactive blog. →
* * *
## Anatomy of a Throttler, part 3
[Engineering]
By Shlomi Noach | November 19, 2024
Design considerations for implementing a database throttler →
* * *
## Introducing sharding on PlanetScale with workflows
[Product]
By Benjamin Dicken | November 7, 2024
Run Vitess workflows right from within PlanetScale. Migrate data from unsharded to sharded keyspaces, manage traffic cutover, and easily revert when problems arise. →
* * *
## Announcing Vitess 21
[Vitess]
By Vitess Engineering Team | October 29, 2024
Vitess 21 is now generally available. →
* * *
## Announcing the PlanetScale vectors public beta
[Product]
By Holly Guevara | October 21, 2024
You can now use the vector data type for vector search and storage in your PlanetScale MySQL database. →
* * *
## Anatomy of a Throttler, part 2
[Engineering]
By Shlomi Noach | October 10, 2024
Design considerations for implementing a database throttler with a comparison of singular vs distributed throttler deployments. →
* * *
## B-trees and database indexes
[Engineering]
By Benjamin Dicken | September 9, 2024
B-trees are used by many modern DBMSs. Learn how they work, how databases use them, and how your choice of primary key can affect index performance. →
* * *
## Instant deploy requests
[Product]
By Shlomi Noach | September 4, 2024
PlanetScale now supports instant DDL. Where eligible, you can run deploy requests that complete near-instantly. →
* * *
## Anatomy of a Throttler, part 1
[Engineering]
By Shlomi Noach | August 29, 2024
Learn about some design considerations for implementing a database throttler. →
* * *
## Increase IOPS and throughput with sharding
[Engineering]
By Benjamin Dicken | August 19, 2024
For big databases, IOPS and throughput can become a bottleneck in database performance. Learn how sharding helps scale out IOPS and throughput beyond the limitations of a single server. →
* * *
## Tracking index usage with Insights
[Product]
By Rafer Hazen | August 14, 2024
Learn about the new PlanetScale Insights index tracking feature. →
* * *
## Zero downtime migrations at petabyte scale
[Vitess]
By Matt Lord | August 13, 2024
Data migrations are a critical part of the database lifecycle, and are sometimes necessary for version upgrades, sharding, or moving to a new platform. In many cases, migrations are painful and error-prone. In this article, we walk through how migrations are performed at PlanetScale, and offer advice on how to improve the migration experience. →
* * *
## Faster backups with sharding
[Engineering]
By Benjamin Dicken | July 30, 2024
Sharding a database comes with many benefits: Scalability, failure isolation, write throughput, and more. However, one of the lesser-known benefits comes from improved backups and restore performance. →
* * *
## Building data pipelines with Vitess
[Vitess]
By Matt Lord | July 29, 2024
Learn the basics of Change Data Capture (CDC) and how to leverage Vitess VStream API to build data pipelines. →
* * *
## The State of Online Schema Migrations in MySQL
[Engineering]
By Shlomi Noach | July 23, 2024
Learn about the options for running non-blocking schema changes natively to MySQL, using Vitess, or other tools →
* * *
## Optimizing aggregation in the Vitess query planner
[Vitess]
By Andres Taylor | July 22, 2024
The Vitess query planner takes multiple passes over a query plan to optimize it as much as possible before execution. A recent tricky bug report led to an improvement in how the optimizer functions. →
← Previous
1234567891011
Next →
## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
⚡ Blazing fast NVMe drives with unlimited IOPS now available. Read about PlanetScale Metal ⚡
Log in
|Get started
|Book a meeting
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Navigation
  * Documentation
  * |
  * Case studies
  * |
  * Features
  * |
  * Blog
  * |
  * Metal
  * |
  * Pricing
  * |
  * Contact


Blog|Product
Table of contents «Close »
#### Table of contents
  * What is Metal?
  * Customers on Metal


Want to learn more about unlimited IOPS w/ Metal, Vitess, horizontal sharding, or Enterprise options?
Talk to Solutions
Get the RSS feed
# Announcing PlanetScale Metal
By Sam Lambert | March 11, 2025
Today we are announcing the general availability of an entirely new class of nodes available on PlanetScale: Metal.
## What is Metal?
Metal instances are powered by locally-attached NVMe SSD drives and fundamentally change the performance/cost ratio for hosting relational databases on AWS and GCP — with unlimited I/O on every `M-` cluster type.
Metal has been in production for 3 months with some of our customers, and it has served over 5 trillion queries across 5 petabytes of storage. Workloads have seen as much as a 65% drop in p99 query latency, alongside 53% cost savings compared to Amazon Aurora.
And it's now available to everyone, today. No waitlist, no previews.
## Customers on Metal
Now let's hand this launch over to some of our customers to share their experiences:
  * Block: Cash App on PlanetScale Metal
  * Intercom: Evolving Intercom's Database Infrastructure: A Progress Update
  * Depot: 8x faster queries on PlanetScale Metal
  * PlanetScale just made the fastest SQL database ever
  * Upgrading PlanetScale Query Insights to Metal


If you want to learn more about how we built Metal, we wrote about it here.
🤘
## Company
AboutBlogChangelogCareers
## Product
Case studiesEnterprisePricing
## Resources
DocumentationSupportStatusTrust Center
## Courses
Database ScalingLearn VitessMySQL for Developers
## Open source
VitessVitess communityGitHub
Privacy | Terms | Cookies | Do Not Share My Personal Information
© 2025 PlanetScale, Inc. All rights reserved.
GitHub | X | LinkedIn | YouTube | Facebook


# Liens externes trouvés
- https://pscale.link/bl
- https://pscale.link/int
- https://pscale.link/dep
- https://pscale.link/metal-theo
- https://planetscalestatus.com
- https://vitess.io/slack
- https://github.com/planetscale
- https://twitter.com/planetscale
- https://www.linkedin.com/company/planetscale
- https://www.youtube.com/planetscale
- https://www.facebook.com/planetscaledata
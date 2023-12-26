Walmart Process Document 

 

Requirements: -  

Fetch all Grocery Products from Walmart website using client given pin code location. 

 

There are 2 pin codes: -  

60564 - Naperville supercentre 

60074 – Pallidinine store 

 

Step1: - Scrape all Category links from Walmart using selenium. 

Step2: - using category links, iterate on category links and using pagination, scrap all product details, scraping micro data Json available in script tag. 

Step3: - Map the upc using Walmart products in alpha pool 2023 database. 

Step4: - Leftover once new products upc will be scraped by sending get request using tls_client on product page. 
Step5: - separate issue products (weight and upc not available) into new excel sheet. And send for qc 

 

Blocker: -captcha issue – press and hold captcha. 

 

Things we have tried: - 

Selenium wire 

Uc Browser 

Simple requests with cookies 

Rotating headers 

Selenium JavaScript  off 

 

Temporary solution: - copy Fresh cookies and paste into code and run the scrapper. 

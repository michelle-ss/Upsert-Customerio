Hi Customer,

We've recently launched a new Customer.io integration script that upserts user data. Currently, the functionality would overwrite existing user attributes in Customer.io with values from the input data file, including null values. We understand you would like to retain the values you have in Customer.io rather than overwriting the null values. Our goal is to prevent unintended data loss.

We can create an enhancement to the script to retain existing values in Customer.io for attributes that are null in the input data files. This would involve checking each user attribute before performing the upsert operation, ensuring that we only update attributes with non-null values. We're estimating it will take 2-3 days with testing to prevent data loss and to ensure the functionality meets your business needs. 

Please let us know if works and if you have any further questions. Thank you!
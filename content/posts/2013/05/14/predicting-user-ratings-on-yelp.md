Date: 2013-05-14
Title: Predicting User Ratings on Yelp
Category: Software
Tags: machine learning, matlab, yelp

Several weeks ago, Yelp launched a [dataset challenge][yelp] and released data on their users and businesses in Phoenix, AZ. The challenge shared some similarities with the Netflix Prize, and I was curious to see if the Alternating Least Squares algorithm that I used for my [Netflix project][netflix]  was versatile enough to be used for predicting business ratings on Yelp. The results were disappointing, but I shall document the process here for my own reference. All of the code used is available in a [git repository][github].

## Transforming the Data

The dataset arrived in a tarball that unpacks into a directory of JSON files. Each JSON file could be imported into MongoDB relatively easily with the following command:

    $> mongoimport --db yelp --collection reviews --drop --file <filename>

However, since Yelp mangled the primary keys before exporting the dataset, we need to change the primary keys to consecutive integers before we can import the data into MatLab as a sparse matrix. This can be done using the following script (also available from the git repository):

<script src="https://gist.github.com/jimjh/5581460.js"></script>

The `reviews` collection may be exported to a CSV file that can be imported into MatLab.

## Decomposing the Matrix

Using a _latent factor model_, we assume that each business has a set of features, and each user has a certain preference for each feature. Then, the rating that a user gives to a business `r_ij` is the dot product of the business's feature vector `b_i` and the user's preferences vector `u_j`. Putting everything together, we get `B × U = R`, where `B` is the features matrix, `U` is the preferences matrix, and `R` is the ratings matrix.

The goal of the alternating least squares algorithm is thus to determine the matrices `B` and `U`, and then use these for predicting unknown ratings. (The full explanation of the model and the algorithm are available in my [project report][netflix].)

Note that the model doesn't know exactly what these features are - it just guesses at a reasonable number of features.

## Measuring the Results
The entire ratings matrix `R` was too large for my Macbook to handle, and I took a random sample of 2000 users and 2000 businesses, which gave me about 1780 known ratings. The model has two parameters: the number of latent factors, and the regularization factor (lambda). I fixed the number of latent factors at 20, and then used 5-fold cross validation to determine the best value for lambda.

The results were as follows:
<table>
  <tr>
    <th>Algorithm</th>
    <th>RMSE</th>
  </tr>
  <tr>
    <td>Plain ALS</td>
    <td>1.4688</td>
  </tr>
  <tr>
    <td>ALS w. Bias</td>
    <td>1.2365</td>
  </tr>
  <tr>
    <td>ALS w. Correction</td>
    <td>1.5045</td>
  </tr>
</table>

## Possible Improvements
The results were disappointing, given that the standard deviation of my sample was only 1.2077. In other words, ALS did worse than simply predicting the mean rating all the time. Other than fixing possible bugs in my code (maybe I somehow permuted the data?), I could potentially modify the algorithm as follows:

- Take into account known features and estimate user preferences for these.
- Use a clustering algorithm on the locations of the businesses, since a user's preference for a business is likely to be affected by its location.

I will post updates here if I figure out what is going wrong.


  [yelp]: https://www.yelp.com/dataset_challenge/dataset
  [netflix]: |static|/downloads/2013/05/12/netflix.pdf
  [github]: https://github.com/jimjh/yelp-dataset-challenge

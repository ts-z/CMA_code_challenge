# CMA Interview Solved

## Problem

As a User I'd like to be able to create custom collections of art from existing exhibitions at the Cleveland Museum of Art

## Solution

A Backend Python based API that prompts the user for search criteria, allows them to select a unique piece of art ('a highlight piece') to retrieve meta data on, and finally create a custom exhibition based off meta data they select

## Process

I began by breaking down the problem into three major sections:

1. Initial search through exhibitions (InitialSearch class)
2. Selection of a highlight piece of art (InitialSearch class)
3. Generation of a custom exhibition based off metadata from the highlight piece of art (RelatedSearch class)

I then proceeded to write the code for each of the specific functions, keeping each function as a pure function which was responsible for one part of the solution. I decided to give the solution some user interactivity through use of inputs and prints to the console. Finally I combined both classes into a single class to be able to call and run the function using simply the Searches().run() method.

After completing the code I ran the program a few times to generate some sample pieces in an Atlas MongoDB and proceeded to comment the code line by line and create the README file.

## Time to Achieve

2 Hours for Backend API Solution
1 Hour for Documentation / Comments

## Client Facing Application

In order to scale up API to a client facing web application where users can select an exhibition, highlight similarity criteria, and receive results I would further the functionality within the InitialSearch().get_initial_collection() method by introducing User controlled options for the search title, dates, and venue. If there is no concern for API calls / call limits than the user interface could call the exhibition API upon each user change, otherwise the API would be executed upon the click of a user button. A user would then be able to scroll through the pieces of art contained within the exhibitions generated and upon hovering over a piece be presented with it's metadata. The metadata would overlay on the image and be presented in the form of buttons which the user could select to generate a customized exhibition.

## Daily Running Process

To run this as a process that executes daily and posts the results to different social media platforms as a piece of content management software would require a few enhancements. If the User wanted the post to just generate a simple image than the InitialSearch class would become obsolete and could be replaced with the addition of Artificial Intelligence (AI) that would generated randomized search criteria until it got a result, ensure that the image hasn't been posted by checking the database which would store the ids of previously posted works of art, and generate a simple tag line based off the artwork's metadata.

If the goals was to generate mini exhibitions based off of existing or previously hosted exhibitions at CMA than the InitialSearch class would be enhanced with the addition of AI to create randomized search criteria. The remaining functionality would remain relatively unchanged, but AI would be utilized to generate a name for the exhibition and ensure that identifying metadata is tagged to the social media posts.

To create a minimum viable client facing product I would remove the 'InitialSearch' Highlight Search functionality from the user's control, and use it to generate random highlighted pieces for users to scroll through.
The User would have two options for actions within the UI:

1. Select an image and have an exhibition be generated for them via the functionality contained within the 'Related Search' class
2. Select up to five images of their own choosing which were generated from the 'InitialSearch' functions

After generating their custom exhibition they would then have the option to name and save the exhibition. There would also be a community driven page which would contain custom exhibitions created by users of the application.
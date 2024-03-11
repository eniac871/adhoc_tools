# GroupAna -- Group Analyzer 

## Introduction
This is a small python script to fetch a signin user's joined Groups and analysis each group's transive members of details. Then it will list all the groups the user directly joined in a desc order, based on how many groups does this group belongs to.
The usage is: when a user join too many groups, it cause some problem because of too many tokens generated. Authentication may fail when access some sites. So user has to remove them from some groups. With the result of this script, user can know which groups are worth to remove based on its transive members of count.
## Usage
pip install the dependency msgraph SDK, then run the script using python directly. The hardest part of this should be install the msgraph SDK.
## To do
It's possible that several groups are same members of another set of groups, so remove user out of one group may not helping. As a next step, we can define another function to simulate how many groups can be removed when select some groups as remove candidate.

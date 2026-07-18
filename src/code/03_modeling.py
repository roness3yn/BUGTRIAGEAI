{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "#Create text column\n",
    "bug_data_filled[\"text\"] = (\n",
    "    bug_data_filled[\"title\"].fillna(\"\") +\n",
    "    \" \" +\n",
    "    bug_data_filled[\"description\"].fillna(\"\")\n",
    ")\n",
    "\n",
    "#Define categorical features\n",
    "x = bug_data_filled[\n",
    "    [\n",
    "        \"text\",\n",
    "        \"error_code\",\n",
    "        \"bug_domain\",\n",
    "        \"bug_category\",\n",
    "        \"environment\",\n",
    "        \"tech_stack\"\n",
    "    ]\n",
    "]\n",
    "\n",
    "#Define y as combination of severity and priority scores\n",
    "y = bug_data_filled[\"severity_priority\"]\n",
    "\n",
    "print(bug_data_filled[\"severity_priority\"].value_counts())\n",
    "print(bug_data_filled.shape)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "#Test-Train Split\n",
    "x_train, x_test, y_train, y_test = train_test_split(\n",
    "    x,\n",
    "    y,\n",
    "    test_size = 0.2, #80/20 split\n",
    "    random_state = 42,\n",
    "    stratify = y\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "#Create processing pipeline\n",
    "preprocessor = ColumnTransformer(\n",
    "    transformers = [\n",
    "        (\n",
    "          \"text\",\n",
    "         TfidfVectorizer(\n",
    "             stop_words = 'english', #Remove common words\n",
    "             max_features = 3000, #Keeps 3000 most informative words\n",
    "             ngram_range = (1, 2), #Uses single and two-word phrases\n",
    "             min_df = 2 #Ignores words that only appear once)\n",
    "         ),\n",
    "         \"text\"\n",
    "        ),\n",
    "\n",
    "        (\n",
    "            \"categorical\",\n",
    "            #Encode features as one numeric array\n",
    "            OneHotEncoder(handle_unknown = \"ignore\"),\n",
    "            [\n",
    "                \"text\",\n",
    "                \"bug_domain\",\n",
    "                \"bug_category\",\n",
    "                \"environment\",\n",
    "                \"tech_stack\",\n",
    "            ]\n",
    "        )\n",
    "    ]\n",
    ")"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

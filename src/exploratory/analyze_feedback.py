import pandas as pd
pd.set_option('display.max_colwidth', None)

feedback=pd.read_csv('customer_feedback.csv')
print(feedback.head())
print(feedback.shape)
print(feedback.columns)
print(feedback.dtypes)

feedback['date']=pd.to_datetime(feedback['date'])
print(feedback.dtypes)

counts=feedback['channel'].value_counts()
print(counts)

counts2=feedback['journey_stage'].value_counts()
print(counts2)

claim_submission=feedback[feedback['journey_stage'] == 'Claim Submission']
print(claim_submission['feedback_text'].head(10))

#AI PRODUCT
#“Before automating classification, I defined a controlled theme taxonomy and manually reviewed a sample to validate the labeling logic.”:
sample = feedback.sample(10, random_state=42)

print(sample[['feedback_text']])

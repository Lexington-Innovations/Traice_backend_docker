
from flask import Flask, jsonify, request
import pickle
import pandas as pd
import os
from flask import request
from scipy.interpolate import interp1d
import numpy as np
import json
import pickle
import math
app = Flask(__name__)

PICKLED_DIR = './csvfiles/pickled/batch'
branch_binned = pickle.load(open(PICKLED_DIR + '/branch_binned.pkl', 'rb'))
branch_binned2 = pickle.load(open(PICKLED_DIR + '/branch_binned2.pkl', 'rb'))
hit_list = pickle.load(open(PICKLED_DIR + '/hit_list.pkl', 'rb'))
hit_list_out = pickle.load(open(PICKLED_DIR + '/hit_list_out.pkl', 'rb'))
hit_list_expanded_out = pickle.load(open(PICKLED_DIR + '/hit_list_expanded_out.pkl', 'rb'))
ia_kri_mapping_out = pickle.load(open(PICKLED_DIR + '/ia_kri_mapping_out.pkl', 'rb'))
df_ia_agg_scored = pickle.load(open(PICKLED_DIR + '/df_ia_agg_scored.2.pkl', 'rb'))
df=pickle.load(open(PICKLED_DIR + '/df_ia_agg.pkl', 'rb'))
wellbeing1 = pickle.load(open(PICKLED_DIR + '/wellbeing.pkl', 'rb'))

print(df_ia_agg_scored)
print(type(df_ia_agg_scored))
print('dsdfsdfsdfsdfsdfsfd',df_ia_agg_scored.to_dict('list'))
@app.route('/hitlist')
def hitlist():
    #hit_list.cast = hit_list.cast.apply(json.loads)
    return hit_list.to_json(orient="records"), 200

@app.route('/branchbinned')
def branchbinned():
    piechart=pd.DataFrame()
    mydic={'H':'High risk (>80%)',
           'M':'Medium risk (50-80%)',
           'L':'Low risk (<50%)'}
    piechart=branch_binned.groupby(['risk_bin']).count().reset_index()
    piechart['risk_bin']=piechart['risk_bin'].map(mydic)
    #del piechart['Branch #']
    return (piechart[['risk_bin','Branch #']].to_json(orient="records")), 200

@app.route('/branchbinned2')
def branchbinned2():
    branch_binned2 = pickle.load(open(PICKLED_DIR + '/branch_binned2.pkl', 'rb'))
    branch_binned2=branch_binned2.sort_values(['IA Risk Score'], ascending=[False])
    return (branch_binned2.to_json(orient="records")), 200

@app.route('/hitlistout')
def hitlistout():
    hit_list_out = pickle.load(open(PICKLED_DIR + '/hit_list_out.pkl', 'rb'))
    hit_list_out=hit_list_out.sort_values(['IA Risk Score'], ascending=[False])
    return (hit_list_out.to_json(orient="records")), 200

@app.route('/treshold/<user>',methods=['GET'])
def hitlistout3(user):
    hit_list_out = pickle.load(open(PICKLED_DIR + '/hit_list_out.pkl', 'rb'))
    hit_list_out=hit_list_out.sort_values(['IA Risk Score'], ascending=[False])
    hit_list_out=hit_list_out[hit_list_out['IA Risk Score']>int(user)/100]
    #hit_list_out['IA Risk Score']=hit_list_out['IA Risk Score'].apply(lambda x:x*100)
    return (hit_list_out.to_json(orient="records")), 200

@app.route('/hitlistout/<user>',methods=['GET'])
def hitlistout2(user):
    hit_list_out = pickle.load(open(PICKLED_DIR + '/hit_list_out.pkl', 'rb'))
    hit_list_out=hit_list_out.sort_values(['IA Risk Score'], ascending=[False])
    hit_list_out2=hit_list_out[hit_list_out['IA ID']==user]
    return (hit_list_out2.to_json(orient="records")), 200

@app.route('/hitlistexpandedout')
def hitlistexpandedout():
    return (hit_list_expanded_out.to_json(orient="records")), 200

@app.route('/cases')
def cases():
    df2=pickle.load(open('./csvfiles/pickled/batch/acct_trades.pkl', 'rb'))
    df3=pickle.load(open('./csvfiles/pickled/batch/df_ia_agg_scored.pkl', 'rb'))
    df3['IA_NAME']=df3.index
    df3.reset_index(drop=True,inplace=True)
    df2['IA_NAME']=df2.IA_NAME.apply(lambda x:x.strip())
    transaction_risk=pd.merge(df2, df3, how="right", on=['IA_NAME', 'IA_NAME'])
    transaction_risk=transaction_risk.sort_values(['risk_score'],ascending=False)
    transaction_copy=transaction_risk
    transaction_copy['Workflow']=np.random.choice(["In Queue","In Progress", "Escalated","Closed"], transaction_copy.shape[0])
    return (transaction_copy.to_json(orient="records")), 200


@app.route('/cases/inprogress')
def inprogress():
    df2=pickle.load(open('./csvfiles/pickled/batch/acct_trades.pkl', 'rb'))
    df3=pickle.load(open('./csvfiles/pickled/batch/df_ia_agg_scored.pkl', 'rb'))
    df3['IA_NAME']=df3.index
    df3.reset_index(drop=True,inplace=True)
    df2['IA_NAME']=df2.IA_NAME.apply(lambda x:x.strip())
    transaction_risk=pd.merge(df2, df3, how="right", on=['IA_NAME', 'IA_NAME'])
    transaction_risk=transaction_risk.sort_values(['risk_score'],ascending=False)
    transaction_copy=transaction_risk
    transaction_copy['Workflow']=np.random.choice(["In Queue","In Progress", "Escalated","Closed"], transaction_copy.shape[0])
    transaction_copy=transaction_copy[transaction_copy['Workflow']=="In Progress"]
    return (transaction_copy.to_json(orient="records")), 200

@app.route('/cases/inqueue')
def inqueue():
    df2=pickle.load(open('./csvfiles/pickled/batch/acct_trades.pkl', 'rb'))
    df3=pickle.load(open('./csvfiles/pickled/batch/df_ia_agg_scored.pkl', 'rb'))
    df3['IA_NAME']=df3.index
    df3.reset_index(drop=True,inplace=True)
    df2['IA_NAME']=df2.IA_NAME.apply(lambda x:x.strip())
    transaction_risk=pd.merge(df2, df3, how="right", on=['IA_NAME', 'IA_NAME'])
    transaction_risk=transaction_risk.sort_values(['risk_score'],ascending=False)
    transaction_copy=transaction_risk
    transaction_copy['Workflow']=np.random.choice(["In Queue","In Progress", "Escalated","Closed"], transaction_copy.shape[0])
    transaction_copy=transaction_copy[transaction_copy['Workflow']=="In Queue"]
    return (transaction_copy.to_json(orient="records")), 200

@app.route('/cases/escalated')
def escalated():
    df2=pickle.load(open('./csvfiles/pickled/batch/acct_trades.pkl', 'rb'))
    df3=pickle.load(open('./csvfiles/pickled/batch/df_ia_agg_scored.pkl', 'rb'))
    df3['IA_NAME']=df3.index
    df3.reset_index(drop=True,inplace=True)
    df2['IA_NAME']=df2.IA_NAME.apply(lambda x:x.strip())
    transaction_risk=pd.merge(df2, df3, how="right", on=['IA_NAME', 'IA_NAME'])
    transaction_risk=transaction_risk.sort_values(['risk_score'],ascending=False)
    transaction_copy=transaction_risk
    transaction_copy['Workflow']=np.random.choice(["In Queue","In Progress", "Escalated","Closed"], transaction_copy.shape[0])
    transaction_copy=transaction_copy[transaction_copy['Workflow']=="Escalated"]
    return (transaction_copy.to_json(orient="records")), 200

@app.route('/cases/closed')
def closed():
    df2=pickle.load(open('./csvfiles/pickled/batch/acct_trades.pkl', 'rb'))
    df3=pickle.load(open('./csvfiles/pickled/batch/df_ia_agg_scored.pkl', 'rb'))
    df3['IA_NAME']=df3.index
    df3.reset_index(drop=True,inplace=True)
    df2['IA_NAME']=df2.IA_NAME.apply(lambda x:x.strip())
    transaction_risk=pd.merge(df2, df3, how="right", on=['IA_NAME', 'IA_NAME'])
    transaction_risk=transaction_risk.sort_values(['risk_score'],ascending=False)
    transaction_copy=transaction_risk
    transaction_copy['Workflow']=np.random.choice(["In Queue","In Progress", "Escalated","Closed"], transaction_copy.shape[0])
    transaction_copy=transaction_copy[transaction_copy['Workflow']=="Closed"]
    return (transaction_copy.to_json(orient="records")), 200

@app.route('/hitlistexpandedout/<user>', methods=['GET'])
def hitlistexpandedout2(user):
    #print('original hit list out expanded',hitlistexpandedout.head())
    print('iaid of hitlistexpandedout is ',user)
    hitlistexpandedout2=hit_list_expanded_out[hit_list_expanded_out['IA ID']==user]
    print("done deal",type(hitlistexpandedout2.head()))        
    #wellbeing1[wellbeing1['IA ID']==user]
    return (hitlistexpandedout2.to_json(orient="records")), 200


@app.route('/iakrimapping')
def iakrimapping():
    return (ia_kri_mapping_out.to_json(orient="records")), 200


@app.route('/iakrimapping/<user>', methods=['GET'])
def iakrimapping2(user):
    iakrimapping2=ia_kri_mapping_out[ia_kri_mapping_out['IA ID']==user]
    return (iakrimapping2.to_json(orient="records")), 200

@app.route('/aggscored')
def aggscored():
    return str(df_ia_agg_scored.to_json(orient="records"))


@app.route('/wellbeing')
def wellbeing():
    return (wellbeing1.to_json(orient="records")), 200

@app.route('/wellbeing2/<user>', methods=['GET'])
def wellbeing2(user):
    print("I'm in")
    print('iaid is ',user)
    wellbeing2=wellbeing1[wellbeing1['IA ID']==user]
    print('passed',wellbeing2.head())

    wellbeing2['fulfillment'] = np.where(wellbeing2['Value']>= 0.2, wellbeing2['Value'], wellbeing2['Value'].mean())
    wellbeing2['anxiety'] = np.where((wellbeing2['Value']>= 0.1) & (wellbeing2['Value']<= 0.2), wellbeing2['Value'], wellbeing2['Value'].mean())
    wellbeing2['judgement'] = np.where((wellbeing2['Value']> 0) & (wellbeing2['Value']<= 0.1), wellbeing2['Value'], wellbeing2['Value'].mean())

    wellbeing2['fulfillment']=wellbeing2['fulfillment'].apply(lambda x: x*100)
    m = interp1d([0,40],[0,100])
    wellbeing2['fulfillment']=wellbeing2['fulfillment'].apply(lambda x: m(x))
    wellbeing2['anxiety']=wellbeing2['anxiety'].apply(lambda x: x*100)
    wellbeing2['anxiety']=wellbeing2['anxiety'].apply(lambda x: m(x))
    wellbeing2['judgement']=wellbeing2['judgement'].apply(lambda x: x*100)
    wellbeing2['judgement']=wellbeing2['judgement'].apply(lambda x: m(x))
            
    #wellbeing1[wellbeing1['IA ID']==user]
    print('boobooboo',wellbeing2[wellbeing2['IA ID']==user].head())
    return (wellbeing2[wellbeing2['IA ID']==user].head().to_json(orient="records")), 200

@app.route('/transaction/<name>', methods=['GET'])
def transaction(name):
    why=df.append(df.describe()[df.describe().index=='mean'])
    why=why.append(df.describe()[df.describe().index=='count'])
    mydic={"Order_type_MARKET_count_under_IA_TM":"KYC changes to higher risk",                
            "Cancelled_Trades_TM":"Cancelled Trades this month",               
            "Pro_Trades_TM":"Number of pro trades",                   
            "Trades_TM":"Total number of trades this month",            
            "Cancelled_Trades_AllTime":"Large value changes",                   
            "Order_type_LIMIT_count_under_IA_TM":"Account churn / excessive trade",             
            "Order_type_LIMIT_count_under_IA_12M":"Excessively high or low trade volume in senior account",  
            "Order_type_STOP_count_under_IA_TM":"Number of new accounts by IA",               
            "Order_type_STOP_count_under_IA_12M":"Similarity of trading between clients and IA pro account", 
            "Pro_Trades_AllTime":"Excessive trading in IA pro account",           
            "Order_type_MARKET_count_under_IA_12M":"Number of trade reversals",                
            "AMOUNT_TM":"Amount received this month",                
            "Trades_AllTime": "All time Trades",                     
            "TRD_COMMISSION_TM"     :      "Trade Commission this month",              
            "Commission_TM"     :        "Commission this month",                  
            "AMOUNT_12M"      :         "Amount received this year",               
            "TRD_COMMISSION_12M"    :       "Trade Commission this year",                
            "Commission_12M"      :       "Commission this year",                   
            "Trades_Under_Different_IA_TM"   :   "Number of trades under different name this month",     
            "Trades_Under_Different_IA_12M"   :  "Number of trades under different name this year ",    
            "Complaints_AllTime"        :   "Number of complaints this year",             
            "Complaints_TM" :  "Number of complaints this month",           
            "Clients_With_More_Than_One_KYC_Change":"Excessive KYC changes"}
    l1=[]
    for i in why.columns:
        #print(i,mydic[i])
        l1.append(mydic[i])
    why.columns=l1
    import numpy as np
    why_modified=why[np.logical_or(why.index==name,why.index=='mean')]
    why_modified=why_modified[['Trade Commission this year','Trade Commission this month','Amount received this year','Amount received this month','Excessive KYC changes','Excessively high or low trade volume in senior account','Cancelled Trades this month','Number of trades under different name this month']]

    for i in why_modified.columns:
        why_modified[i] = why_modified[i].apply(lambda x: math.ceil(x))

    return why_modified.to_json(orient="index"), 200
    


@app.route('/api/predict', methods=['POST'])
def predict():
    print('one')
    login_json = request.get_json()

    if not login_json:
        return jsonify({'msg': 'Missing JSON'}), 400

    step = login_json.get('step')
    type1 = login_json.get('type')
    amount=login_json.get('amount')
    newbalanceDest= login_json.get('newbalanceDest')
    oldbalanceDest=login_json.get('oldbalanceDest')
    newbalanceOrig=login_json.get('newbalanceOrig')
    oldbalanceOrg=login_json.get('oldbalanceOrg')

    if not step:
        return jsonify({'prediction': 'step is missing'}), 400

    if not type1:
        return jsonify({'prediction': 'type is missing'}), 400


    if not amount:
        return jsonify({'prediction': 'amount is missing'}), 400

    if not newbalanceDest:
        return jsonify({'prediction': 'newbalancedest is missing'}), 400


    if not oldbalanceDest:
        return jsonify({'prediction': 'oldbalanceDest is missing'}), 400

    if not newbalanceOrig:
        return jsonify({'prediction': 'newbalanceOrig is missing'}), 400
    
    if not oldbalanceOrg:
        return jsonify({'prediction': 'oldbalanceOrg is missing'}), 400
    

    
    x_unit_test=pd.DataFrame([[int(step),type1,float(amount),float(oldbalanceOrg),float(newbalanceOrig),float(oldbalanceDest),float(newbalanceDest)]],columns=['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
       'oldbalanceDest', 'newbalanceDest'])
    unique_types=['CASH_IN', 'PAYMENT', 'TRANSFER', 'CASH_OUT', 'DEBIT']

    for each_categorical_value in unique_types:
        #x_unit_test[each_categorical_value]=0
        #print(each_categorical_value)
        if(x_unit_test['type'][0]==each_categorical_value):
            x_unit_test[each_categorical_value]=1
        else:
            x_unit_test[each_categorical_value]=0
        #x_unit_test[each_categorical_value]=pd.get_dummies
    x_unit_test=x_unit_test[['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig',
       'oldbalanceDest', 'newbalanceDest','CASH_IN','PAYMENT', 'TRANSFER', 'CASH_OUT',
       'DEBIT']]
    x_unit_test.drop(columns=['type'],inplace=True)
    print('prediction1',x_unit_test.head())
    sc=pickle.load(open('../../traice_moneylaundering/scaler.pkl','rb'))
    x_unit_test_scales=sc.transform(x_unit_test)
    rf=pickle.load(open('../../traice_moneylaundering/GradientBoostingClassifier()_best_model.pkl','rb'))
    print('prediction3',x_unit_test.head())
    prediction=rf.predict_proba(x_unit_test_scales)[:,1]*100
    print('prediction4',prediction)
    return jsonify({'prediction': str(prediction[0])}), 200

@app.route('/flag', methods=['GET', 'POST'])
def flag():
    if request.method == 'POST':
        print('looooooooooollllllll',request.form['flag'])
        df_frame=pd.DataFrame();
        df_frame["flag"]=[request.form["flag"]]
        df_frame["case_id"]=[request.form["case_id"]]
        df_frame.to_csv('flagged_cases.csv', mode='a', header=False)
    return "flagged record  added"

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0',port=5005)


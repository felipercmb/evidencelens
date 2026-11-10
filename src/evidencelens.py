"""Transparent, dependency-free review-priority classifier. Not a truth detector."""
import math, re
from review import analyze
FEATURES = ['missing_word_fraction','missing_number_fraction','negation_mismatch','answer_length_ratio','empty_evidence']
def tokens(text): return re.findall(r"[a-z]+|\d+(?:\.\d+)?", text.lower())
def features(evidence, answer):
    e,a=set(tokens(evidence)),set(tokens(answer))
    en=set(re.findall(r'\b\d+(?:\.\d+)?\b', evidence)); an=set(re.findall(r'\b\d+(?:\.\d+)?\b', answer))
    neg={'not','never','no','cannot'}
    return [len(a-e)/max(1,len(a)),len(an-en)/max(1,len(an)),float(bool(a&neg)!=bool(e&neg)),min(3,len(tokens(answer))/max(1,len(tokens(evidence)))),float(not e)]
def sigmoid(z): return 1/(1+math.exp(-max(-40,min(40,z))))
def fit(rows, epochs=1400, lr=.12):
    w=[0.]*len(FEATURES); b=0.
    xs=[features(r['evidence'],r['answer']) for r in rows]; ys=[r['label'] for r in rows]
    for _ in range(epochs):
        dw=[0.]*len(w); db=0.
        for x,y in zip(xs,ys):
            err=sigmoid(sum(v*q for v,q in zip(w,x))+b)-y
            for j in range(len(w)): dw[j]+=err*x[j]
            db+=err
        w=[v-lr*(g/len(xs)+.005*v) for v,g in zip(w,dw)]; b-=lr*db/len(xs)
    return {'weights':w,'bias':b,'feature_names':FEATURES,'threshold':.5,'status':'synthetic_prototype_not_real_world_validated'}
def predict(model,evidence,answer):
    x=features(evidence,answer); p=sigmoid(sum(v*q for v,q in zip(model['weights'],x))+model['bias'])
    return {**analyze(evidence,answer), 'review_score':p,'decision':'review' if p>=model['threshold'] else 'lower_priority','features':dict(zip(FEATURES,x)), 'model_status':model['status'], 'limitations':'Treinado apenas em exemplos sintéticos em inglês. Score não calibrado: não é probabilidade de erro. Baixa prioridade não garante verdade. Não compreende semântica nem valida fontes.'}
def metrics(ys, ps):
    pred=[p>=.5 for p in ps]; tp=sum(y and p for y,p in zip(ys,pred)); fp=sum(not y and p for y,p in zip(ys,pred)); fn=sum(y and not p for y,p in zip(ys,pred)); tn=sum(not y and not p for y,p in zip(ys,pred))
    return {'n':len(ys),'accuracy':(tp+tn)/len(ys),'precision':tp/max(1,tp+fp),'recall':tp/max(1,tp+fn),'f1':2*tp/max(1,2*tp+fp+fn),'brier':sum((y-p)**2 for y,p in zip(ys,ps))/len(ys),'confusion':{'tp':tp,'fp':fp,'fn':fn,'tn':tn}}

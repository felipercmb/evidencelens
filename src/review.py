"""Conservative local evidence alignment. Rules are alerts, never factual verdicts."""
import re,unicodedata
STOP=set('a an the is are was were to of in on and or for with it as at o a os as um uma de da do das dos em no na nos nas e ou para por com que é são foi'.split())
NEG=set('not never cannot no neither without não nunca jamais nem sem'.split())
def normalize(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFC',s).casefold()).strip().rstrip('.!?;')
def words(s): return re.findall(r'[^\W\d_]+',normalize(s),re.UNICODE)
def sentences(text):
    # Keep decimal separators inside a sentence; split newlines and punctuation before whitespace.
    return [s.strip() for s in re.split(r'(?<=[.!?;])\s+|\n+',text) if s.strip()]
def numbers(text): return re.findall(r'(?<!\w)[+-]?\d+(?:[.,]\d+)*(?:\s*%)?',text)
def content(s): return set(words(s))-STOP-NEG
def similarity(a,b):
    x,y=content(a),content(b)
    return len(x&y)/max(1,len(x|y))
def analyze(evidence,answer):
    sources=sentences(evidence); claims=[]
    for sentence in sentences(answer):
        exact=next((s for s in sources if normalize(s)==normalize(sentence)),None)
        ranked=sorted(sources,key=lambda s:similarity(sentence,s),reverse=True)
        best=exact or (ranked[0] if ranked else '')
        signals=[];status='abstain'; reason='Não foi possível estabelecer suporte. Compare com a fonte e revise manualmente.'
        sim=similarity(sentence,best)
        if exact:
            status='matched';reason='Frase literalmente presente no texto fornecido. Isso não verifica a veracidade da fonte.'
        elif best and sim>=.30:
            newnums=set(numbers(sentence))-set(numbers(best))
            if newnums: signals.append('Números sem correspondência no trecho selecionado: '+', '.join(sorted(newnums)))
            if bool(set(words(sentence))&NEG)!=bool(set(words(best))&NEG): signals.append('Presença de negação diferente entre os trechos; confirme o escopo.')
            aw,bw=words(sentence),words(best)
            if set(aw)==set(bw) and aw!=bw: signals.append('Mesmas palavras em ordem diferente; papéis e relações podem ter mudado.')
            if signals:
                status='review';reason='Há diferenças específicas para uma pessoa conferir. Não são prova automática de contradição.'
        claims.append({'text':sentence,'status':status,'evidence':best,'reason':reason,'signals':signals})
    counts={s:sum(c['status']==s for c in claims) for s in ['review','abstain','matched']}
    overall='review' if counts['review'] else ('abstain' if counts['abstain'] or not claims else 'matched')
    return {'overall_status':overall,'claims':claims,'summary':counts,'engine':'conservative_alignment_v2','policy':'Nenhuma resposta é aprovada automaticamente. A correspondência é textual, não factual.'}

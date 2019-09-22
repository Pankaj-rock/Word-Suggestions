from django.shortcuts import render
from suggestions import server
from nltk.corpus import brown
from nltk.corpus import PlaintextCorpusReader
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import JsonResponse


new_corpus = PlaintextCorpusReader('./','.*')
tokens = brown.words() + new_corpus.words('my_corpus.txt')
# print("+++++++++++++tokens+++++++",type(tokens))
bgs_freq = server.get_bigram_freq(tokens)
tgs_freq = server.get_trigram_freq(tokens)



def output(request):
    # string1=request.POST.get("string")
    # original_pred=[]
    # pred1=request.POST.get("pred1")
    # pred2=request.POST.get("pred2")
    # pred3=request.POST.get("pred3")
    # work=request.POST.get("work")
    # pred=server.worker(string1)
    # print("@@@@@@@@@@@@@@@@@@@@PRED_JSON@@@@@@@@@@@@@@@@@@",pred)
    # print("_________________________REQ_______________",request)

    return render(request,"index.html")


# @ensure_csrf_cookie
def worker(request):
    #string ="i am not"
    if request.method=="GET":
        # print("__________________REQUEST__________",request)
        string=request.GET.get("string")
        # print("_________STRING________",string)
        words=string.split()
        # print("_______________WORDS_________________",words)
        n=len(words)
        # print("_________________LENGTH___________",n)

        if n==1:
            # print("______________bgs_____________",bgs_freq[(string)].most_common(5))
            predict=bgs_freq[(string)].most_common(5)
            # print("_________PREDICT_____________",predict)
            # try:
            #     a=json.dumps(predict)
            #     print("_____________A>JSON________",a)
            # except:
            #     print("__________________ERROR HERE_____________")

            return JsonResponse({"predict":predict})
            # return json.dumps(bgs_freq[(string)].most_common(5))

        elif n>1:
            print(words[n-2],words[n-1])
            # print("_____________________tgs________________",tgs_freq[(words[n-2],words[n-1])].most_common(5))

            predict=tgs_freq[(words[n-2],words[n-1])].most_common(5)
            # print("_________PREDICT_____________",predict)
            return JsonResponse({"predict":predict})
            # return json.dumps(tgs_freq[(words[n-2],words[n-1])].most_common(5))
            # if work=='pred':
            #     if n==1:
            #         #print (bgs_freq[(string)].most_common(5),file=sys.stderr)
            #
            #         return json.dumps(bgs_freq[(string)].most_common(5))
            #
            #     elif n>1:
            #         #print (tgs_freq[(words[n-2],words[n-1])].most_common(5),file=sys.stderr)
            #
            #         return json.dumps(tgs_freq[(words[n-2],words[n-1])].most_common(5))
        else:
            predict=server.incomplete_pred(words, n)
            # print("_________PREDICT_____________",predict)
            return JsonResponse({"predict":predict})
            # return json.dumps(incomplete_pred(words, n))
    # print("__________________PRED_WORD__________________",pred_word)
    # return pred_word

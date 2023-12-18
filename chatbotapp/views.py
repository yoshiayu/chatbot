from django.shortcuts import render
from django.http import HttpResponse # 追記
from transformers import AutoModelForQuestionAnswering, BertJapaneseTokenizer
import torch


model_name = 'KoichiYasuoka/bert-base-japanese-wikipedia-ud-head'
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

def home(request):
    """
    http://127.0.0.1:8000/で表示されるページ
    """
    # return render(request, 'chatbot/home.html')
    return render(request, '/Users/yoshiayu/Desktop/work/sample/chatbot/chatbotapp/templates/home.html')     

def reply(question):
    tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
    expanded_context = "私の名前は山田です。趣味は動画鑑賞とショッピングです。年齢は30歳で、出身は大阪府です。職業は医者で、特に小児科に関心があります。好きな食べ物は寿司とラーメンで、休日はよく友達と食事に行きます。最近読んだ本は「未来の医療」で、医療技術の進化について学んでいます。また、旅行が好きで、最後に訪れたのは京都でした。"

    # 特定のキーワードに基づく応答
    if "趣味" in question:
        return "動画鑑賞とショッピングが大好きなんだ。あなたはどんな趣味があるの？"
    elif "好きな食べ物" in question:
        return "寿司とラーメン、どちらもたまらなく好きなんだよ。あなたのおすすめの料理は何かな？"
    elif "旅行" in question:
        return "京都に行ったときのこと、すごく楽しかったなあ。あなたのお気に入りの旅行先はどこ？"
    elif "映画" in question:
        return "映画は大好きだよ。特にアクション映画がお気に入り。あなたはどんな映画が好き？"
    elif "仕事" in question:
        return "医者として働いているよ。毎日が挑戦だけど、とてもやりがいがあるんだ。あなたの仕事は何？"
    elif "読書" in question:
        return "最近は「未来の医療」って本を読んだよ。医療技術の進歩について書かれていて、とても興味深かったな。あなたはどんな本を読むのが好き？"

    else:
    # デフォルトのBERTモデルによる回答
        inputs = tokenizer.encode_plus(question, expanded_context, add_special_tokens=True, return_tensors="pt")
        input_ids = inputs["input_ids"].tolist()[0]
        output = model(**inputs)
        answer_start = torch.argmax(output.start_logits)
        answer_end = torch.argmax(output.end_logits) + 1
        answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
        return "ねえ、聞いてくれて嬉しいよ。" + answer.replace(' ', '') + " こんな感じかな？"


def bot_response(request):
    """
    HTMLフォームから受信したデータを返す処理
    http://127.0.0.1:8000/bot_response/として表示する
    """

    input_data = request.POST.get('input_text')
    if not input_data:
        return HttpResponse('<h2>空のデータを受け取りました。</h2>', status=400)

    bot_response = reply(input_data)
    http_response = HttpResponse()
    http_response.write(f"BOT: {bot_response}")

    return http_response

# def reply(question):

#     tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)

#     context = "私の名前は山田です。趣味は動画鑑賞とショッピングです。年齢は30歳です。出身は大阪府です。仕事は医者です。"
#     inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]
#     output = model(**inputs)
#     answer_start = torch.argmax(output.start_logits)  
#     answer_end = torch.argmax(output.end_logits) + 1 
#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     answer = answer.replace(' ', '')

#     return answer
#  context = "はい、お手伝いします。それは興味深い質問ですね。申し訳ありませんが、その質問には答えられません。もちろん、どうぞ。それについては少し調べる必要があります。\
#         それは私の専門外ですが、お役に立てるかもしれません。そのトピックについては詳しくないですが、興味深いですね。それについては異なる意見があります。はい、その通りです。\
#             いいえ、それは正しくないかもしれません。それは確認する必要がありますね。おっしゃる通りです。それは少し難しい質問ですね。それについては、もう少し情報が必要です。\
#                 それは面白い考えですね。私も同意見です。それには複数の見方があります。それは私には答えられませんが、他の情報源を探してみてください。それは私の知識の範囲外です。それについては詳しい情報がありません。"
# from django.shortcuts import render
# from django.http import HttpResponse
# from transformers import AutoModelForQuestionAnswering, BertJapaneseTokenizer
# import torch
# from django.views.generic import TemplateView

# model_name = 'KoichiYasuoka/bert-base-japanese-wikipedia-ud-head'
# model = AutoModelForQuestionAnswering.from_pretrained(model_name)
# tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)


# # Create your views here.

# def home(request):
#     """
#     http://127.0.0.1:8000/で表示されるページ
#     """
#     return render(request, 'home.html')


# def reply(question):

#     tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)

#     context = "私の名前は山田です。趣味は動画鑑賞とショッピングです。年齢は30歳です。出身は大阪府です。仕事は医者です。"
#     inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")
#     input_ids = inputs["input_ids"].tolist()[0]
#     output = model(**inputs)
#     answer_start = torch.argmax(output.start_logits)  
#     answer_end = torch.argmax(output.end_logits) + 1 
#     answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))
#     answer = answer.replace(' ', '')
#     answer = "".join(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))


#     return answer


# def bot_response(request):
#     """
#     HTMLフォームから受信したデータを返す処理
#     http://127.0.0.1:8000/bot_response/として表示する
#     """

#     input_data = request.POST.get('input_text')
#     if not input_data:
#         return HttpResponse('<h2>空のデータを受け取りました。</h2>', status=400)

#     bot_response = reply(input_data)
#     http_response = HttpResponse()
#     http_response.write(f"BOT: {bot_response}")

#     return http_response

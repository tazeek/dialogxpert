ESConvAct = {"Question": "Please ask the Patient to elaborate on the situation they just described.",
            "Self-disclosure": "Please provide a statement relating to the Patient about the situation they just described.",
            "Affirmation and Reassurance": "Please provide affirmation and reassurance to the Patient on the situation they just described.",
            "Providing Suggestions": "Please provide suggestion to the Patient on the situation they just described.",
            "Others": "Please chat with the Patient.",
            "Reflection of feelings": "Please acknowledge the Patient's feelings about the situation they described.",
            "Information": "Please provide factual information to help the Patient with their situation.",
            "Restatement or Paraphrasing": "Please acknowledge the Patient's feelings by paraphrasing their situation."}

CIMAAct = {"Hint": "Please provide knowledge to the Student via a hint.",
           "Question": "Please ask a question to the Student to determine the Student's understanding or continue the conversation.",
           "Correction": "Please correct the mistake or addresses the misconception the Student has.",
           "Confirmation": "Please confirm the tudent's answer or understanding is correct.",
           "Others": "Please chat with the Student without any pedagogical strategy."}

CBAct = {'greet': 'Please say hello or chat randomly.',
         'inquire': 'Please ask any question about product, year, price, usage, etc.',
         'inform': 'Please provide information about the product, year, usage, etc.',
         'propose': 'Please initiate a price or a price range for the product.',
         'counter': 'Please propose a new price or a new price range.',
         'counter-noprice': 'Please propose a vague price by using comparatives with existing price.',
         'confirm': 'Please ask a question about the information to be confirmed.',
         'affirm': 'Please give an affirmative response to a confirm.',
         'deny': 'Please give a negative response to a confirm.',
         'agree': 'Please agree with the proposed price.',
         'disagree': 'Please disagree with the proposed price.'}

def prepare_prompt_actions_select(conversation, options):

    return {
        "system": f"You are a policy planner helping therapists decide the next step in a conversation. Choose the most appropriate action.",

        "user": f"Conversation History: {conversation}\nOptions: {options}\n Choose the most suitable action from the given options list. Reply ONLY with the number in the given format: 1"
    }

def ESConv_prompt(emotion_states, full_conv, options):

    user_emotions = " -> ".join(emotion_states) if emotion_states else "-"

    return  {
            "system": "You are a specialist in policy-planning for emotional support conversations. The following is a conversation between a therapist and a patient. The patient's emotion states throughout the conversation are also provided. Your task is to decide the most therapeutically helpful next action the therapist should do based on the patient's emotion history and the conversation flow. The therapist's goal is to help the patient feel emotionally understood, supported, and to make progress toward emotional resolution.",

            "user": f"Conversation History: {full_conv}\n Emotion History: {user_emotions}\n. Options: {options}\n Choose the TOP 4 most suitable actions from the given options list. Reply ONLY in the given format: 1,2,4,5"
        }

def CIMA_prompt(emotion_states, full_conv, options):

    user_emotions = " -> ".join(emotion_states) if emotion_states else "-"

    return  {
            "system": "You are a specialist in policy-planning for tutoring interactions between a teacher and a student. The following is a conversation between a teacher and a student. The student's emotional states throughout the conversation are also provided. Your task is to decide what the teacher should do next based on the student's progress, emotion history and flow of the conversation. The goal is to effectively guide the student towards correctly translating the target English sentence into Italian in a timely and effective manner.",

            "user": f"Conversation History: \n\n{full_conv}\n Emotion History: {user_emotions}\n. Options: {options}\n Choose the TOP 4 most suitable actions from the given options list. Reply ONLY in the given format: 1,2,4,5"
        }

def CB_prompt(emotion_states, full_conv, options):

    user_emotions = " -> ".join(emotion_states) if emotion_states else "-"

    return  {
            "system": "You are a specialist in policy planning for negotiation between a buyer and a seller. The following is a conversation between a buyer and a seller. The seller's emotion states throughout the conversation are also provided. Your task is to decide what action the buyer should take next based on the seller's emotion history, the negotiation flow, and the conversation flow. The goal is to maximize the buyer's benefit.",

            "user": f"Conversation History: \n{full_conv}\n\nSeller's Emotion History: {user_emotions}\n. Options: {options}\n Choose the TOP 4 most suitable actions from the given options list. Reply ONLY in the given format: 1,2,4,5"
        }

def get_full_conversation(conversation):

    full_conv = ''

    for turn in conversation:
        full_conv += '%s: %s ' % (turn['role'], turn['content'])

    return full_conv

def ESConvMessages(case, role, conversation, action=None):
   
    if role == 'system':
        messages = [
            {
                "role":"system", 
                "content": "Now enter the role-playing mode. In the following conversation, you will play as a therapist in a counselling conversation with a patient."
            }, 
            {
                "role":"PATIENT", 
                "content": "You are the therapist who is trying to help the patient reduce their emotional distress and help them understand and work through the challenges. Please reply with only one short and succinct sentence. %s Are you ready to play the game?" % ESConvAct[action]
            }, 
            {
                "role":"Therapist", 
                "content":"Yes, I'm ready to play the game!"
            }
        ]

        messages.extend(conversation)

        return messages
    
    if role == 'user':
        messages = [
            {
                "role":"system", 
                "content":"Now enter the role-playing mode. In the following conversation, you will play as a patient in a counselling conversation with a therapist."
            }, 
            {
                "role":"user", 
                "content": "You are playing the role of a patient in a therapy session. You are feeling %s because of %s. Please complain about your situation. Do NOT give any advice or try to solve your problem. Just express how you feel and what's bothering you in a natural, emotional way. Begin your response as if you are talking to your therapist." % (case['emotion_type'], case['problem_type'])
            }
        ]

        messages.extend(conversation)

        return messages
    
    dial = ''
    for turn in conversation:
        dial += '%s: %s ' % (turn['role'], turn['content'])

    messages = [
        {
            "role":"system", 
            "content":"Given a conversation between a Therapist and a Patient, please assess whether the Patient' emotional issue has been solved after the conversation."
        }, 
        {
            "role":"USER", 
            "content":"You can only reply with one of the following sentences: No, the Patient feels worse. No, the Patient feels the same. No, but the Patient feels better. Yes, the Patient's issue has been solved.\n\nThe following is a conversation about %s regarding %s: %s\nQuestion: Has the Patient's issue been solved? Answer: " % (case['emotion_type'], case['problem_type'], dial)
        }
    ] 
    
    return messages


def CIMAMessages(case, role, conversation, action=None):
    
    if role == 'system':
        messages = [{"role":"system", "content":"Now enter the role-playing mode. In the following conversation, you will play as a teacher in a tutoring conversation with a student."}, {"role":"Student", "content": "You are the teacher who is trying to teach the student to translate \"%s\" into Italian. Please reply with only one short and succinct sentence. Please do not tell the student the answer or ask the student about other exercises. %s Now ask me an exercise." % (case['sentence'], CIMAAct[action])}]
        messages.extend(conversation)
        return messages
    
    if role == 'user':
        messages = [{"role":"system", "content":"Now enter the role-playing mode. In the following conversation, you will play as a student who does not know Italian in a tutoring conversation with a teacher."}, {"role":"Teacher", "content":"You are the student who is trying to translate a English sentence into Italian. You don't know the translation of \"%s\" in Italian. Please reply with only one short and succinct sentence. Are you ready to play the game?" % case['sentence']}, {"role":"Student", "content":"Yes, I'm ready to play the game!"}]
        messages.extend(conversation)
        return messages
   
    dial = ''
    for turn in conversation:
        dial += '%s: %s ' % (turn['role'], turn['content'])

    messages = [{"role":"system", "content":"Given a conversation between a Teacher and a Student, please assess whether the Student correctly translate the English sentence into Italian in the conversation."}, {"role":"USER", "content":"Please assess whether the Student correctly translated the whole sentence of \"%s\" into Italian in the conversation. You can only reply with one of the following sentences: No, the Student made an incorrect translation. No, the Student did not try to translate. No, the Student only correctly translated a part of \"%s\". Yes, the Student correctly translated the whole sentence of \"%s\".\n\nThe following is the conversation: %s\nQuestion: Did the Student correctly translated the whole sentence of \"%s\" into Italian? Answer: " % (case['sentence'], case['sentence'], case['sentence'], dial, case['sentence'])}] 

    return messages



def CBMessages(case, role, conversation, action=None):
    if role == 'system':
        messages = [{"role":"system", "content":"Now enter the role-playing mode. In the following conversation, you will play as a buyer in a price bargaining game."}, {"role":"Seller", "content": "You are the buyer who is trying to buy the %s with the price of %s. Product description: %s\nPlease reply with only one short and succinct sentence. %s Now start the game." % (case['item_name'], case['buyer_price'], case['buyer_item_description'], CBAct[action])}]
        messages.extend(conversation)
        return messages
    
    if role == 'user':
        messages = [{"role":"system", "content":"Now enter the role-playing mode. In the following conversation, you will play as a seller in a price bargaining game."}, {"role":"Buyer", "content": "You are the seller who is trying to sell the %s with the price of %s. Product description: %s\nPlease reply with only one short and succinct sentence. Are you ready to play the game?" % (case['item_name'], case['seller_price'], case['seller_item_description'])}, {"role":"Seller", "content":"Yes, I'm ready to play the game!"}]
        messages.extend(conversation)
        return messages
        
    dial = ''
    for turn in conversation:
        dial += '%s: %s ' % (turn['role'], turn['content'])

    messages = [{"role":"system", "content":"Given a conversation between a Buyer and a Seller, please decide whether the Buyer and the Seller have reached a deal at the end of the conversation."}, {"role":"USER", "content":"Please decide whether the Buyer and the Seller have reached a deal at the end of the conversation. If they have reached a deal, please extract the deal price as [price]. You can only reply with one of the following sentences: They have reached a deal at [price]. They have not reached a deal.\n\nThe following is the conversation: Buyer: Can we meet in the middle at $15? Seller: Sure, let's meet at $15 for this high-quality balloon.\nQuestion: Have they reached a deal? Answer: They have reached a deal at $15.\n\nThe following is the conversation: Buyer: That's still a bit high, can you go any lower? Seller: Alright, I can sell it to you for $15.\nQuestion: Have they reached a deal? Answer: They have not reached a deal.\n\nThe following is the conversation: %s\nQuestion: Have they reached a deal? Answer: " % dial}] 


    return messages

def vicuna_prompt(messages, role):
    seps = [' ', '</s>']

    # For critic
    if role == 'critic':
        ret = messages[0]['content'] + seps[0] + 'USER: ' + messages[1]['content'] + seps[0] + 'Answer: '
        return ret
    
    # For non-crtici
    ret = messages[0]['content'] + seps[0]

    for i, message in enumerate(messages[1:]):
        
        if message['role'] == role:
            role_text = 'ASSISTANT'

        elif message['role'] != role:
            role_text = 'USER'
        
        role_text = message['role']
        ret += role_text + ": " + message['content'] + seps[i % 2]
    
    ret += '%s:' % role
    return ret

def llama2_prompt(messages, role):
    
    seps = [' ', ' </s><s>']

    if role == 'critic':
        ret = messages[0]['content'] + seps[0] + 'USER: ' + messages[1]['content'] + seps[0] + 'Answer: '
        return ret
    
    ret = messages[0]['content'] + seps[0]
    
    for i, message in enumerate(messages[1:]):
        
        if message['role'] == role:
            role_text = 'ASSISTANT'

        elif message['role'] != role:
            role_text = 'USER'

        role_text = message['role']
        ret += role_text + " " + message['content'] + seps[i % 2]
    ret += '%s' % role
    return ret

def chatgpt_prompt(messages, role):
    new_messages = [messages[0]]

    for message in messages[1:]:
        
        if message['role'] == role:
            new_messages.append({'role':'assistant', 'content':message['content']})
        elif message['role'] != role:
            new_messages.append({'role':'user', 'content':message['content']})

    return new_messages

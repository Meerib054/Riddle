import requests
import streamlit as st
import time


st.header("🧩 THIS IS A GAME OF RIDDLES 🧩")
st.write("")
st.write("(note that all the answers are of two words)")
st.write("you have 4 tries per riddle")

def main():
    if "saved_riddles" not in st.session_state:
        st.session_state.saved_riddles = None
    if st.session_state.saved_riddles is None:
        num = st.number_input("Number of riddles:", value=1, step=1)
        if st.button("Submit"):
            st.session_state.saved_riddles = num
            st.rerun()
        st.stop()
    total_riddles = st.session_state.saved_riddles
    st.write(f"The number of riddle is: {total_riddles}")

    if "riddles" not in st.session_state:
        st.session_state.riddles = riddle(total_riddles)
    riddles = st.session_state.riddles

    if "current" not in st.session_state:
        st.session_state.current = 0

    if "score" not in st.session_state:
        st.session_state.score = 0


    if st.session_state.current<total_riddles:
        result=answer(riddles[st.session_state.current])

        if result is True:
            st.session_state.score=score(st.session_state.score)
            st.session_state.pop(f"answer_{st.session_state.current}", None)
            st.session_state.current+=1
            st.rerun()
        
        elif result is False:
            st.session_state.pop(f"answer_{st.session_state.current}", None)
            st.session_state.current+=1
            st.rerun()

    else:
        st.success("Game Over!")
        st.write(f"Final Score: {st.session_state.score}/{total_riddles}")
        effects(st.session_state.score,total_riddles)




def riddle(desired_count):
    lis = []
    while len(lis) < desired_count:
        get_requests = requests.get("https://riddles-api.vercel.app/random")
        get_requests.raise_for_status()
        get_j = get_requests.json()

        answer_text = get_j["answer"].strip()
        word_count = len(answer_text.split())

        if  word_count == 2:
            lis.append({"riddle": get_j["riddle"], "answer": answer_text.lower()})

    return lis


def answer(file):
    if "tries" not in st.session_state:
        st.session_state.tries=3

    if st.session_state.tries <= 0:
        st.error(f"The correct answer was: {file['answer']}")
        
        if st.button("Next Riddle"):
            st.session_state.tries = 3
            return False  
            
        return None

    st.write(file["riddle"])
    ans = st.text_input("Answer:", key=f"answer_{st.session_state.current}")

    pronoun=["my","our","a","the","in","their","your"]

    if st.button("Check Answer"):
        if file["answer"].startswith(tuple(pronoun)):
            x=file["answer"].split()
            y=ans.split()
            if len(x)>1 and len(y)>1 and x[1]==y[1]:
                st.session_state.tries=3
                return True
        elif ans.lower().strip() == file['answer'].lower():
            st.session_state.tries = 3
            return True
        else:
            st.session_state.tries -= 1
            


def score(points):
    return points + 1


def effects(score, total):
    if score==0:
       st.snow()
       st.error("Try better next time!")

    elif total==score:
        st.success("YAY! ☆")
        st.balloons()
        time.sleep(1)
        st.balloons()
        time.sleep(1)
        st.balloons()
    
    else:
        st.snow()
        st.warning("Not bad")


if __name__ == "__main__":
    main()

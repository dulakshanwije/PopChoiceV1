import { useState } from "react";
import Button from "../Button/Button";
import styles from "./form.module.css";
import axios from "axios";

export default function Form({ setResponse }) {
  const initialAnswerSet = {
    answer1: "",
    answer2: "",
    answer3: "",
  };
  const [answerSet, setAnswerSet] = useState(initialAnswerSet);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);

    const query = {
      1: {
        question: "What’s your favorite movie and why?",
        answer: answerSet.answer1,
      },
      2: {
        question: "Are you in the mood for something new or a classic?",
        answer: answerSet.answer2,
      },
      3: {
        question: "Do you wanna have fun or do you want something serious?",
        answer: answerSet.answer3,
      },
    };

    try {
      const response = await axios.post("http://127.0.0.1:5000/suggest/", {
        content: query,
      });
      const suggest = response.data.content;
      if (suggest.success == true) {
        setResponse(suggest);
      } else {
        const response = {
          name: "Error 💔",
          description: suggest.error,
        };
        setResponse(response);
      }
    } catch (error) {
      console.log(error);
      const response = {
        name: "Error 💔",
        description: "Something went wrong!",
      };
      setResponse(response);
    } finally {
      setIsLoading(false);
      setAnswerSet(initialAnswerSet);
    }
  }

  return (
    <>
      <div>
        <form className={styles.form} id="form" onSubmit={handleSubmit}>
          <div className={styles.inputContainer}>
            <div className={styles.inputBox}>
              <p>What’s your favorite movie and why?</p>
              <textarea
                disabled={isLoading}
                rows={3}
                required
                value={answerSet.answer1}
                onChange={(e) =>
                  setAnswerSet({ ...answerSet, answer1: e.target.value })
                }
              ></textarea>
            </div>
            <div className={styles.inputBox}>
              <p>Are you in the mood for something new or a classic?</p>
              <textarea
                disabled={isLoading}
                rows={3}
                required
                value={answerSet.answer2}
                onChange={(e) =>
                  setAnswerSet({ ...answerSet, answer2: e.target.value })
                }
              ></textarea>
            </div>
            <div className={styles.inputBox}>
              <p>Do you wanna have fun or do you want something serious?</p>
              <textarea
                disabled={isLoading}
                rows={3}
                required
                value={answerSet.answer3}
                onChange={(e) =>
                  setAnswerSet({ ...answerSet, answer3: e.target.value })
                }
              ></textarea>
            </div>
          </div>
          <Button
            type="submit"
            disabled={isLoading}
            value={isLoading ? "Guessing..." : "Let's Go"}
          />
        </form>
      </div>
    </>
  );
}

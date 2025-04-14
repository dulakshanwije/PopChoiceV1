import Button from "../Button/Button";
import styles from "./description.module.css";

export default function Description({ name, description, setResponse }) {
  function goAgain() {
    setResponse({});
  }

  return (
    <div className={styles.container}>
      <p className={styles.name}>{name}</p>
      <p className={styles.description}>{description}</p>
      <Button type="button" value={"Go Again!"} onClick={goAgain} />
    </div>
  );
}

import logo from "/src/assets/images/PopChoice.svg";
import styles from "./header.module.css";
export default function Header() {
  return (
    <div className={styles.container}>
      <img src={logo} alt="" className={styles.image} />
      <p className={styles.title}>PopChoice</p>
    </div>
  );
}

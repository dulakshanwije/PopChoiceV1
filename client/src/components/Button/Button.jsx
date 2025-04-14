import styles from "./button.module.css";
export default function Button({
  value,
  type = "button",
  onClick,
  disabled = false,
}) {
  return (
    <button
      className={styles.button}
      type={type}
      onClick={onClick}
      disabled={disabled}
    >
      {value}
    </button>
  );
}

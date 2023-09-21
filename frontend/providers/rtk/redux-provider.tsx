import { store } from "@/store/store";
import { Provider } from "react-redux";

type ReduxProps = {
  children: React.ReactNode;
};

export const ReduxProvider = ({ children }: ReduxProps) => {
  return <Provider store={store}>{children}</Provider>;
};

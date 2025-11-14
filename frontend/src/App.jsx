import "./App.css";
import Footer from "./components/Footer";
import Header from "./components/Header";

function App({ children }) {
  return (
    <div className="app-container">
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  );
}

export default App;

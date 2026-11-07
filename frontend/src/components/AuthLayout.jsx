import ProductDiagram from "./ProductDiagram";
import HowItWorks from "./HowItWorks";
import SiteFooter from "./SiteFooter";

// The frame around the log in and register pages.
export default function AuthLayout({ children }) {
  return (
    <div className="site">
      <a className="skip" href="#main">
        Skip to content
      </a>
      <header className="topbar">
        <div className="wrap">
          <span className="brand">StudyBuddy</span>
        </div>
      </header>
      <main id="main">
        <div className="wrap hero">
          <div>
            <p className="eyebrow">Campus peer tutoring</p>
            <p className="lead">
              Find a tutor who has done well in your course, book a session, and pay safely.
            </p>
            {children}
          </div>
          <div className="hero-visual">
            <ProductDiagram />
          </div>
        </div>
        <HowItWorks />
      </main>
      <SiteFooter />
    </div>
  );
}

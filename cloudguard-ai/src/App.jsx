function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-6 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-blue-500">
          CloudGuard AI
        </h1>

        <div className="flex gap-6">
          <a href="#">Features</a>
          <a href="#">Dashboard</a>
          <a href="#">About</a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="flex flex-col items-center text-center py-32 px-6">
        <h1 className="text-6xl font-bold max-w-4xl">
          AI-Powered AWS Security Auditor
        </h1>

        <p className="text-slate-400 text-xl mt-6 max-w-2xl">
          Detect cloud risks, analyze security threats, and get AI-powered remediation recommendations.
        </p>

        <div className="mt-10 flex gap-4">
          <button className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl font-semibold">
            Start Scanning
          </button>

          <button className="border border-slate-700 px-6 py-3 rounded-xl">
            Learn More
          </button>
        </div>
      </section>

      {/* Features Card */}
      <section className="grid md:grid-cols-3 gap-6 px-8 pb-20">

        <div className="bg-slate-900 p-6 rounded-2xl">
          <h3 className="text-xl font-bold mb-3">
            AWS Security Scan
          </h3>
          <p className="text-slate-400">
            Detect risky cloud configurations and exposed resources.
          </p>
        </div>

        <div className="bg-slate-900 p-6 rounded-2xl">
          <h3 className="text-xl font-bold mb-3">
            AI Risk Analysis
          </h3>
          <p className="text-slate-400">
            Understand threats in plain English with AI explanations.
          </p>
        </div>

        <div className="bg-slate-900 p-6 rounded-2xl">
          <h3 className="text-xl font-bold mb-3">
            Automated Reports
          </h3>
          <p className="text-slate-400">
            Generate audit reports and remediation suggestions instantly.
          </p>
        </div>

      </section>

      {/* Stats Section */}
      <section className="py-20 px-8">
        <div className="grid md:grid-cols-3 gap-6 text-center">

          <div>
            <h2 className="text-4xl font-bold text-blue-500">500+</h2>
            <p className="text-slate-400">Resources Scanned</p>
          </div>

          <div>
            <h2 className="text-4xl font-bold text-blue-500">95%</h2>
            <p className="text-slate-400">Detection Accuracy</p>
          </div>

          <div>
            <h2 className="text-4xl font-bold text-blue-500">60%</h2>
            <p className="text-slate-400">Faster Audits</p>
          </div>

        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-8">
        <h2 className="text-4xl font-bold text-center mb-12">
          How CloudGuard AI Works
        </h2>

        <div className="grid md:grid-cols-4 gap-6">

          <div className="bg-slate-900 p-6 rounded-2xl">
            <h3 className="font-bold text-xl mb-2">
              1. Connect AWS
            </h3>
            <p className="text-slate-400">
              Securely connect your AWS environment.
            </p>
          </div>

          <div className="bg-slate-900 p-6 rounded-2xl">
            <h3 className="font-bold text-xl mb-2">
              2. Scan Resources
            </h3>
            <p className="text-slate-400">
              Analyze S3, IAM and EC2 configurations.
            </p>
          </div>

          <div className="bg-slate-900 p-6 rounded-2xl">
            <h3 className="font-bold text-xl mb-2">
              3. AI Analysis
            </h3>
            <p className="text-slate-400">
              AI explains risks and business impact.
            </p>
          </div>

          <div className="bg-slate-900 p-6 rounded-2xl">
            <h3 className="font-bold text-xl mb-2">
              4. Get Fixes
            </h3>
            <p className="text-slate-400">
              Receive remediation suggestions instantly.
            </p>
          </div>

        </div>
      </section>

      {/* Dashboard Preview */}
      <section className="py-24 px-8">

        <h2 className="text-4xl font-bold text-center mb-4">
          Security Dashboard Preview
        </h2>

        <p className="text-center text-slate-400 mb-12">
          Monitor threats, vulnerabilities, and cloud security posture in real-time.
        </p>

        <div className="max-w-6xl mx-auto bg-slate-900 rounded-3xl p-8 border border-slate-800">

          <div className="grid md:grid-cols-4 gap-6">

            <div className="bg-slate-800 p-6 rounded-2xl">
              <h3 className="text-slate-400">
                Security Score
              </h3>

              <p className="text-4xl font-bold text-blue-500 mt-2">
                78
              </p>
            </div>

            <div className="bg-slate-800 p-6 rounded-2xl">
              <h3 className="text-slate-400">
                Critical Issues
              </h3>

              <p className="text-4xl font-bold text-red-500 mt-2">
                3
              </p>
            </div>

            <div className="bg-slate-800 p-6 rounded-2xl">
              <h3 className="text-slate-400">
                Medium Risks
              </h3>

              <p className="text-4xl font-bold text-yellow-500 mt-2">
                8
              </p>
            </div>

            <div className="bg-slate-800 p-6 rounded-2xl">
              <h3 className="text-slate-400">
                Resources Scanned
              </h3>

              <p className="text-4xl font-bold text-green-500 mt-2">
                512
              </p>
            </div>

          </div>

          <div className="mt-8 bg-slate-800 p-6 rounded-2xl">
            <h3 className="text-xl font-bold mb-4">
              AI Security Recommendation
            </h3>

            <p className="text-slate-300">
              Public access detected on S3 bucket "company-data". Disable public access and enforce bucket policies to prevent unauthorized exposure.
            </p>
          </div>

        </div>

      </section>

    </div>
  );
}

export default App;
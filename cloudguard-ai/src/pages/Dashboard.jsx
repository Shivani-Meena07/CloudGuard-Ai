function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      {/* PAGE TITLE */}
      <h1 className="text-4xl font-bold mb-8">
        Security Dashboard
      </h1>

      {/* SECURITY SCORE CARD */}
      <div className="bg-slate-900 p-6 rounded-2xl shadow-lg">
        <h2 className="text-xl mb-2">
          Security Score
        </h2>

        <p className="text-5xl font-bold text-blue-500">
          78/100
        </p>

        <p className="text-slate-400 mt-2">
          Overall cloud security health score
        </p>
      </div>

      {/* FINDINGS SECTION */}
      <div className="grid md:grid-cols-3 gap-6 mt-8">

        {/* HIGH RISK */}
        <div className="bg-red-900/20 border border-red-500 p-6 rounded-xl">
          <h3 className="text-xl font-bold">
            🚨 Public S3 Bucket
          </h3>

          <p className="text-red-300 mt-2">
            High Risk
          </p>
        </div>

        {/* MEDIUM RISK */}
        <div className="bg-yellow-900/20 border border-yellow-500 p-6 rounded-xl">
          <h3 className="text-xl font-bold">
            ⚠ Open Security Group
          </h3>

          <p className="text-yellow-300 mt-2">
            Medium Risk
          </p>
        </div>

        {/* MEDIUM RISK */}
        <div className="bg-yellow-900/20 border border-yellow-500 p-6 rounded-xl">
          <h3 className="text-xl font-bold">
            ⚠ Excessive IAM Permissions
          </h3>

          <p className="text-yellow-300 mt-2">
            Medium Risk
          </p>
        </div>

      </div>

      {/* AI SECURITY ASSISTANT */}
      <div className="bg-slate-900 p-6 rounded-2xl mt-8 shadow-lg">

        <h2 className="text-2xl font-bold mb-4">
          AI Security Assistant
        </h2>

        <p className="text-slate-300 leading-relaxed">
          The bucket "company-data" is publicly accessible and may expose
          sensitive information. Disable public access and enable bucket
          policies immediately to reduce the risk of unauthorized access.
        </p>

      </div>

    </div>
  );
}

export default Dashboard;
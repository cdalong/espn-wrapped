import React, { useState } from 'react';
import { Trophy, TrendingUp, TrendingDown, Target, Star, AlertTriangle, Zap, Users, BarChart3 } from 'lucide-react';

const FantasyBasketballWrapped = () => {
  const [credentials, setCredentials] = useState({
    league_id: '',
    year: 2025,
    espn_s2: '',
    swid: ''
  });
  const [isInitialized, setIsInitialized] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [stats, setStats] = useState({});

  const API_BASE = 'http://localhost:8000';

  const handleInitialize = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE}/initialize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          league_id: parseInt(credentials.league_id),
          year: credentials.year,
          espn_s2: credentials.espn_s2,
          swid: credentials.swid
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to initialize. Please check your credentials.');
      }

      setIsInitialized(true);
      await loadAllStats();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchStat = async (endpoint) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`);
      if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`);
      return await response.text();
    } catch (err) {
      console.error(`Error fetching ${endpoint}:`, err);
      return 'Error loading data';
    }
  };

  const loadAllStats = async () => {
    setLoading(true);
    const endpoints = [
      '/team/find-trae',
      '/team/weekly-average',
      '/team/best-week',
      '/team/worst-week',
      '/team/longest-streak',
      '/team/sleeper',
      '/team/bust',
      '/team/clutch',
      '/team/best-matchup',
      '/team/worst-matchup'
    ];

    const results = {};
    for (const endpoint of endpoints) {
      results[endpoint] = await fetchStat(endpoint);
    }
    
    setStats(results);
    setLoading(false);
  };

  const StatCard = ({ icon: Icon, title, value, description, color = "blue" }) => {
    const colorClasses = {
      blue: "bg-gradient-to-br from-blue-500 to-blue-600 text-white",
      green: "bg-gradient-to-br from-green-500 to-green-600 text-white",
      red: "bg-gradient-to-br from-red-500 to-red-600 text-white",
      purple: "bg-gradient-to-br from-purple-500 to-purple-600 text-white",
      orange: "bg-gradient-to-br from-orange-500 to-orange-600 text-white",
      yellow: "bg-gradient-to-br from-yellow-400 to-yellow-500 text-white"
    };

    return (
      <div className={`p-6 rounded-xl shadow-lg transform hover:scale-105 transition-all duration-300 ${colorClasses[color]}`}>
        <div className="flex items-center justify-between mb-4">
          <Icon className="h-8 w-8 opacity-80" />
          <div className="text-right">
            <h3 className="text-lg font-semibold opacity-90">{title}</h3>
          </div>
        </div>
        <div className="space-y-2">
          <p className="text-2xl font-bold">{value}</p>
          {description && <p className="text-sm opacity-80">{description}</p>}
        </div>
      </div>
    );
  };

  if (!isInitialized) {
    return (
      <div 
        className="min-h-screen flex items-center justify-center p-4"
        style={{
          backgroundImage: `url('/tyrese.jpg')`,
          backgroundSize: '50% 100%', // Each image takes half the width, full height
          backgroundPosition: '0% 50%, 100% 50%', // Position images side by side
          backgroundRepeat: 'repeat-x' // Repeat horizontally to ensure two instances
        }}
      >
        <div className="w-full max-w-md">
          <div className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-white/20">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="h-8 w-8 text-white" />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">Fantasy Basketball Wrapped</h1>
              <p className="text-white/70">Enter your ESPN Fantasy credentials to get started</p>
            </div>

            {error && (
              <div className="bg-red-500/20 border border-red-500/50 text-red-100 p-4 rounded-lg mb-6">
                {error}
              </div>
            )}

            <div className="space-y-4">
              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">League ID</label>
                <input
                  type="number"
                  value={credentials.league_id}
                  onChange={(e) => setCredentials({...credentials, league_id: e.target.value})}
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="Your league ID"
                />
              </div>

              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">Year</label>
                <input
                  type="number"
                  value={credentials.year}
                  onChange={(e) => setCredentials({...credentials, year: parseInt(e.target.value)})}
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                />
              </div>

              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">ESPN_S2</label>
                <input
                  type="text"
                  value={credentials.espn_s2}
                  onChange={(e) => setCredentials({...credentials, espn_s2: e.target.value})}
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="Your ESPN_S2 cookie"
                />
              </div>

              <div>
                <label className="block text-white/80 text-sm font-medium mb-2">SWID</label>
                <input
                  type="text"
                  value={credentials.swid}
                  onChange={(e) => setCredentials({...credentials, swid: e.target.value})}
                  className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                  placeholder="Your SWID cookie"
                />
              </div>

              <button
                onClick={handleInitialize}
                disabled={loading || !credentials.league_id || !credentials.espn_s2 || !credentials.swid}
                className="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-orange-600 hover:to-orange-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02]"
              >
                {loading ? 'Loading...' : 'Get My Wrapped'}
              </button>
            </div>

            <div className="mt-6 text-center">
              <p className="text-white/60 text-sm">
                Need help finding your cookies?{' '}
                <a href="#" className="text-orange-400 hover:text-orange-300 underline">
                  Check the guide
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="min-h-screen p-4"
      style={{
        backgroundImage: `url('/tyrese.jpg')`,
        backgroundSize: '50% 100%', // Each image takes half the width, full height
        backgroundPosition: '0% 50%, 100% 50%', // Position images side by side
        backgroundRepeat: 'repeat-x' // Repeat horizontally to ensure two instances
      }}
    >
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <BarChart3 className="h-10 w-10 text-white" />
          </div>
          <h1 className="text-5xl font-bold text-white mb-4">Your Fantasy Basketball Wrapped</h1>
          <p className="text-xl text-white/70 max-w-2xl mx-auto">
            A deep dive into your {credentials.year} fantasy basketball season
          </p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-500"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            <StatCard
              icon={Target}
              title="Trae Young Hunt"
              value={stats['/team/find-trae'] || 'Loading...'}
              color="orange"
            />

            <StatCard
              icon={BarChart3}
              title="Weekly Average"
              value={stats['/team/weekly-average'] ? `${parseFloat(stats['/team/weekly-average']).toFixed(1)} pts` : 'Loading...'}
              description="Points per week"
              color="blue"
            />

            <StatCard
              icon={Trophy}
              title="Best Week"
              value={stats['/team/best-week'] || 'Loading...'}
              description="Your highest scoring week"
              color="green"
            />

            <StatCard
              icon={TrendingDown}
              title="Worst Week"
              value={stats['/team/worst-week'] || 'Loading...'}
              description="Room for improvement"
              color="red"
            />

            <StatCard
              icon={TrendingUp}
              title="Longest Streaks"
              value={stats['/team/longest-streak'] || 'Loading...'}
              description="Win and loss streaks"
              color="purple"
            />

            <StatCard
              icon={Star}
              title="Sleeper Star"
              value={stats['/team/sleeper'] || 'Loading...'}
              description="Exceeded expectations"
              color="yellow"
            />

            <StatCard
              icon={AlertTriangle}
              title="Biggest Bust"
              value={stats['/team/bust'] || 'Loading...'}
              description="Underperformed projections"
              color="red"
            />

            <StatCard
              icon={Zap}
              title="Clutch Player"
              value={stats['/team/clutch'] || 'Loading...'}
              description="Came through when needed"
              color="orange"
            />

            <StatCard
              icon={Users}
              title="Best Matchup"
              value={stats['/team/best-matchup'] || 'Loading...'}
              description="Your favorite opponent"
              color="green"
            />

            <StatCard
              icon={Users}
              title="Worst Matchup"
              value={stats['/team/worst-matchup'] || 'Loading...'}
              description="Your kryptonite team"
              color="red"
            />
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 pb-8">
          <button
            onClick={() => {
              setIsInitialized(false);
              setStats({});
              setCredentials({ league_id: '', year: 2025, espn_s2: '', swid: '' });
            }}
            className="bg-white/10 backdrop-blur-sm text-white px-6 py-3 rounded-lg border border-white/20 hover:bg-white/20 transition-all duration-200"
          >
            Enter Different League
          </button>
        </div>
      </div>
    </div>
  );
};

export default FantasyBasketballWrapped;
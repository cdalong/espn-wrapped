import React, { useState, useEffect } from 'react';
import { Trophy, TrendingUp, TrendingDown, Target, Star, AlertTriangle, Zap, Users, BarChart3, ChevronLeft, ChevronRight } from 'lucide-react';

const FantasyBasketballWrapped = () => {
  const [credentials, setCredentials] = useState({
    league_id: '',
    year: 2025,
    espn_s2: '',
    swid: '',
    username: '',
    password: ''
  });
  const [authMethod, setAuthMethod] = useState('cookies'); // 'cookies' or 'login'
  const [isInitialized, setIsInitialized] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [stats, setStats] = useState({});
  const [currentPage, setCurrentPage] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [hoveredTitle, setHoveredTitle] = useState(null);

  const API_BASE = 'http://localhost:8000';

  // Title explanations mapping
  const titleExplanations = {
    'underdog': 'Overperformed your projected total points',
    'overrated': 'Underperformed your projected total points', 
    'cakewalk': 'Biggest positive difference in PF vs PA',
    'toughie': 'Biggest negative difference in PF vs PA',
    'quick hands': 'You had the most pick-ups throughout the league',
    'longest win streak': 'Stellar performance!',
    'longest loss streak': 'Maybe next year is your year',
    'participation trophy': 'Uh, at least you showed up and had fun!'
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
      '/team/worst-matchup',
      '/team/biggest-comeback',
      '/team/bonus-titles',
      '/team/missing-points'
    ];

    try {
      const results = await Promise.all(
        endpoints.map(endpoint => fetchStat(endpoint))
      );
      
      const statsData = {
        trae: results[0],
        weeklyAverage: results[1],
        bestWeek: results[2],
        worstWeek: results[3],
        longestStreak: results[4],
        sleeper: results[5],
        bust: results[6],
        clutch: results[7],
        bestMatchup: results[8],
        worstMatchup: results[9],
        biggestComeback: results[10],
        bonusTitles: results[11],
        missingPoints: results[12]
      };
      
      setStats(statsData);
    } catch (err) {
      setError('Failed to load stats: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleInitialize = async () => {
    setLoading(true);
    setError('');
    
    try {
      const requestBody = {
        league_id: parseInt(credentials.league_id),
        year: credentials.year,
      };

      // Add authentication fields based on selected method
      if (authMethod === 'cookies') {
        requestBody.espn_s2 = credentials.espn_s2;
        requestBody.swid = credentials.swid;
      } else {
        requestBody.username = credentials.username;
        requestBody.password = credentials.password;
      }

      const response = await fetch(`${API_BASE}/initialize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to initialize. Please check your credentials.');
      }

      setIsInitialized(true);
      await loadAllStats();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = () => {
    if (!credentials.league_id) return false;
    
    if (authMethod === 'cookies') {
      return credentials.espn_s2 && credentials.swid;
    } else {
      return credentials.username && credentials.password;
    }
  };

  // Helper function to clean and format stat data
  const formatStat = (statValue) => {
    if (!statValue || statValue === 'Loading...' || statValue === 'Error loading data') {
      return statValue;
    }
    
    // Remove quotes if they exist
    let cleaned = statValue.replace(/^["']|["']$/g, '');
    
    // Check if it's structured data (contains colons and commas)
    if (cleaned.includes(':') && cleaned.includes(',')) {
      return parseStructuredData(cleaned);
    }
    
    return cleaned;
  };

  // Helper function to parse structured data like "Data a: 10, data b: 20"
  const parseStructuredData = (data) => {
    const parts = data.split(',').map(part => part.trim());
    return parts.map((part, index) => {
      const [label, value] = part.split(':').map(s => s.trim());
      return { label, value, index };
    });
  };

  // Component to render structured data nicely
  const StructuredDataDisplay = ({ data }) => {
    if (Array.isArray(data)) {
      return (
        <div className="space-y-4">
          {data.map((item, index) => (
            <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
              <div className="text-lg text-white/80 capitalize">{item.label}</div>
              <div className="text-3xl font-bold text-white">{item.value}</div>
            </div>
          ))}
        </div>
      );
    }
    return <div className="text-6xl font-bold text-white">{data}</div>;
  };

  // Enhanced Title Badge Component with Tooltip
  const TitleBadge = ({ title, index }) => {
    const titleKey = title.label ? title.label.toLowerCase() : title.toLowerCase();
    const titleText = title.label || title;
    const explanation = titleExplanations[titleKey];

    return (
      <div 
        key={index} 
        className="relative inline-block"
        onMouseEnter={() => setHoveredTitle(index)}
        onMouseLeave={() => setHoveredTitle(null)}
      >
        <div className="bg-white/10 backdrop-blur-sm rounded-full px-6 py-3 border border-white/20 cursor-pointer hover:bg-white/20 transition-all duration-200 hover:scale-105">
          <div className="text-lg font-semibold text-white capitalize">{titleText.trim()}</div>
        </div>
        
        {/* Tooltip */}
        {hoveredTitle === index && explanation && (
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-4 py-2 bg-gray-900/95 backdrop-blur-sm text-white text-sm rounded-lg border border-white/20 max-w-xs text-center z-10 animate-in fade-in duration-200">
            <div className="font-medium mb-1 capitalize">{titleText.trim()}</div>
            <div className="text-white/80 text-xs leading-relaxed">{explanation}</div>
            {/* Arrow */}
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900/95"></div>
          </div>
        )}
      </div>
    );
  };

  const pages = [
    {
      title: "Welcome to Your Season",
      subtitle: `${credentials.year} Fantasy Basketball Wrapped`,
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <BarChart3 className="h-16 w-16 text-white" />
          </div>
          <p className="text-xl text-white/80 max-w-2xl mx-auto">
            Let's dive into your fantasy basketball journey this season. 
            From your biggest wins to your most surprising picks, we've got it all covered.
          </p>
        </div>
      )
    },
    {
      title: "The Trae Young Hunt",
      subtitle: "Your quest for greatness",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Target className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.trae)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Every fantasy manager has their white whale. Here's how your hunt went this season.
          </p>
        </div>
      )
    },
    {
      title: "Weekly Consistency",
      subtitle: "Your scoring average",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <BarChart3 className="h-16 w-16 text-white" />
          </div>
          <div className="text-6xl font-bold text-white mb-4">
            {stats.weeklyAverage ? `${parseFloat(formatStat(stats.weeklyAverage)).toFixed(1)}` : 'Loading...'}
          </div>
          <div className="text-2xl text-white/80 mb-8">points per week</div>
          <p className="text-xl text-white/80 max-w-2xl mx-auto">
            Consistency is key in fantasy basketball. This was your average weekly performance.
          </p>
        </div>
      )
    },
    {
      title: "Peak Performance",
      subtitle: "Your best week",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Trophy className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.bestWeek)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Remember this week? Everything clicked. Your lineup was fire, and the points kept coming.
          </p>
        </div>
      )
    },
    {
      title: "Learning Moment",
      subtitle: "Your toughest week",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <TrendingDown className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.worstWeek)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Every champion has their low points. This week tested your resolve, but you bounced back stronger.
          </p>
        </div>
      )
    },
    {
      title: "Streak Master",
      subtitle: "Your longest runs",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-purple-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <TrendingUp className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.longestStreak)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Momentum is everything. Here are your longest winning and losing streaks this season.
          </p>
        </div>
      )
    },
    {
      title: "Hidden Gem",
      subtitle: "Your sleeper pick",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-full flex items-center justify-center mx-auto mb-8">
            <Star className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.sleeper)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            While others slept, you saw the potential. This player exceeded all expectations.
          </p>
        </div>
      )
    },
    {
      title: "The Disappointment",
      subtitle: "Your biggest bust",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <AlertTriangle className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.bust)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            High expectations, low returns. Even the best drafters have their misses.
          </p>
        </div>
      )
    },
    {
      title: "Clutch Factor",
      subtitle: "Your reliable performer",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-orange-500 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Zap className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.clutch)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            When the pressure was on, this player delivered. Your most dependable fantasy asset.
          </p>
        </div>
      )
    },
    {
      title: "Favorite Matchup",
      subtitle: "Your preferred opponent",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Users className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.bestMatchup)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Some matchups just click. This opponent brought out the best in your lineup.
          </p>
        </div>
      )
    },
    {
      title: "Toughest Opponent",
      subtitle: "Your kryptonite",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Users className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.worstMatchup)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Every hero has their nemesis. This team always seemed to have your number.
          </p>
        </div>
      )
    },
    {
      title: "Greatest Comeback",
      subtitle: "Your most dramatic turnaround",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <TrendingUp className="h-16 w-16 text-white" />
          </div>
          <StructuredDataDisplay data={formatStat(stats.biggestComeback)} />
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            Down but not out! This was your most impressive comeback victory of the season.
          </p>
        </div>
      )
    },
    {
      title: "Special Achievements",
      subtitle: "Your season honors",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Trophy className="h-16 w-16 text-white" />
          </div>
          <div className="text-center">
            {(() => {
              const titles = formatStat(stats.bonusTitles);
              if (Array.isArray(titles)) {
                return (
                  <div className="flex flex-wrap justify-center gap-3">
                    {titles.map((title, index) => (
                      <TitleBadge key={index} title={title} index={index} />
                    ))}
                  </div>
                );
              } else if (typeof titles === 'string') {
                return (
                  <div className="flex flex-wrap justify-center gap-3">
                    {titles.split(',').map((title, index) => (
                      <TitleBadge key={index} title={title.trim()} index={index} />
                    ))}
                  </div>
                );
              }
              return <div className="text-6xl font-bold text-white">{titles}</div>;
            })()}
          </div>
          <p className="text-xl text-white/80 max-w-2xl mx-auto mt-8">
            These are the special achievements you earned throughout the season! <br />
            <span className="text-sm text-white/60">Hover over each title to learn more about what it means</span>
          </p>
        </div>
      )
    },
    {
      title: "Points Left Behind",
      subtitle: "Your bench production",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-orange-400 to-orange-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <AlertTriangle className="h-16 w-16 text-white" />
          </div>
          <div className="text-6xl font-bold text-white mb-4">
            {stats.missingPoints ? parseFloat(formatStat(stats.missingPoints)).toFixed(1) : 'Loading...'}
          </div>
          <div className="text-2xl text-white/80 mb-8">points on the bench</div>
          <p className="text-xl text-white/80 max-w-2xl mx-auto">
            These are the points you left on your bench when you had empty lineup spots. 
            Setting your lineup is crucial!
          </p>
        </div>
      )
    },
    {
      title: "Season Complete",
      subtitle: "Thanks for playing!",
      content: (
        <div className="text-center">
          <div className="w-32 h-32 bg-gradient-to-br from-purple-400 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-8">
            <Trophy className="h-16 w-16 text-white" />
          </div>
          <p className="text-xl text-white/80 max-w-2xl mx-auto mb-8">
            Another season in the books! Whether you won it all or learned valuable lessons, 
            every season makes you a better fantasy manager.
          </p>
          <button
            onClick={() => {
              setIsInitialized(false);
              setStats({});
              setCredentials({ league_id: '', year: 2025, espn_s2: '', swid: '', username: '', password: '' });
              setCurrentPage(0);
            }}
            className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-purple-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
          >
            Try Another League
          </button>
        </div>
      )
    }
  ];

  const nextPage = () => {
    if (currentPage < pages.length - 1) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentPage(currentPage + 1);
        setIsTransitioning(false);
      }, 150);
    }
  };

  const prevPage = () => {
    if (currentPage > 0) {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentPage(currentPage - 1);
        setIsTransitioning(false);
      }, 150);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      nextPage();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      prevPage();
    }
  };

  useEffect(() => {
    if (isInitialized) {
      window.addEventListener('keydown', handleKeyPress);
      return () => window.removeEventListener('keydown', handleKeyPress);
    }
  }, [currentPage, isInitialized]);

  if (!isInitialized) {
    return (
      <div 
        className="min-h-screen flex items-center justify-center p-4"
        style={{
          backgroundImage: `url('/tyrese.jpg')`,
          backgroundSize: '50% 100%',
          backgroundPosition: '0% 50%, 100% 50%',
          backgroundRepeat: 'repeat-x'
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

            {/* Authentication Method Selector */}
            <div className="mb-6">
              <div className="flex bg-white/5 rounded-lg p-1">
                <button
                  onClick={() => setAuthMethod('cookies')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all duration-200 ${
                    authMethod === 'cookies' 
                      ? 'bg-orange-500 text-white shadow-md' 
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  }`}
                >
                  Cookies
                </button>
                <button
                  onClick={() => setAuthMethod('login')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-all duration-200 ${
                    authMethod === 'login' 
                      ? 'bg-orange-500 text-white shadow-md' 
                      : 'text-white/70 hover:text-white hover:bg-white/10'
                  }`}
                >
                  Username/Password
                </button>
              </div>
            </div>

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

              {/* Conditional Authentication Fields */}
              {authMethod === 'cookies' ? (
                <>
                  <div>
                    <label className="block text-white/80 text-sm font-medium mb-2">
                      ESPN_S2 Cookie
                      <span className="text-orange-400 ml-1">*</span>
                    </label>
                    <input
                      type="text"
                      value={credentials.espn_s2}
                      onChange={(e) => setCredentials({...credentials, espn_s2: e.target.value})}
                      className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                      placeholder="Your ESPN_S2 cookie"
                    />
                  </div>

                  <div>
                    <label className="block text-white/80 text-sm font-medium mb-2">
                      SWID Cookie
                      <span className="text-orange-400 ml-1">*</span>
                    </label>
                    <input
                      type="text"
                      value={credentials.swid}
                      onChange={(e) => setCredentials({...credentials, swid: e.target.value})}
                      className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                      placeholder="Your SWID cookie"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div>
                    <label className="block text-white/80 text-sm font-medium mb-2">
                      ESPN Username
                      <span className="text-orange-400 ml-1">*</span>
                    </label>
                    <input
                      type="text"
                      value={credentials.username}
                      onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                      className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                      placeholder="Your ESPN username"
                      autoComplete="username"
                    />
                  </div>

                  <div>
                    <label className="block text-white/80 text-sm font-medium mb-2">
                      ESPN Password
                      <span className="text-orange-400 ml-1">*</span>
                    </label>
                    <input
                      type="password"
                      value={credentials.password}
                      onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                      className="w-full p-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-orange-500"
                      placeholder="Your ESPN password"
                      autoComplete="current-password"
                    />
                  </div>
                </>
              )}

              <button
                onClick={handleInitialize}
                disabled={loading || !isFormValid()}
                className="w-full bg-gradient-to-r from-orange-500 to-orange-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-orange-600 hover:to-orange-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02]"
              >
                {loading ? 'Connecting to ESPN...' : 'Get My Wrapped'}
              </button>
            </div>

            <div className="mt-6 text-center">
              <p className="text-white/60 text-sm">
                {authMethod === 'cookies' ? (
                  <>
                    Need help finding your cookies?{' '}
                    <a href="#" className="text-orange-400 hover:text-orange-300 underline">
                      Check the guide
                    </a>
                  </>
                ) : (
                  <>
                    Use your regular ESPN login credentials
                  </>
                )}
              </p>
              <p className="text-white/50 text-xs mt-2">
                Your credentials are only used to access your fantasy data and are not stored.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="min-h-screen flex flex-col p-4 relative"
      style={{
        backgroundImage: `url('/tyrese.jpg')`,
        backgroundSize: '50% 100%',
        backgroundPosition: '0% 50%, 100% 50%',
        backgroundRepeat: 'repeat-x'
      }}
    >
      {loading ? (
        <div className="flex-1 flex justify-center items-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-500"></div>
        </div>
      ) : (
        <>
          {/* Main Content Area - Takes up available space */}
          <div className="flex-1 flex items-center justify-center">
            <div className="w-full max-w-4xl mx-auto">
              <div className={`text-center transition-all duration-300 ${isTransitioning ? 'opacity-0 transform scale-95' : 'opacity-100 transform scale-100'}`}>
                <h1 className="text-5xl font-bold text-white mb-4">
                  {pages[currentPage].title}
                </h1>
                <h2 className="text-2xl text-white/70 mb-12">
                  {pages[currentPage].subtitle}
                </h2>
                
                <div>
                  {pages[currentPage].content}
                </div>
              </div>
            </div>
          </div>

          {/* Fixed Navigation Area - Always at bottom */}
          <div className="flex-shrink-0 mt-8">
            <div className="w-full max-w-4xl mx-auto">
              {/* Navigation */}
              <div className="flex justify-between items-center mb-6">
                <button
                  onClick={prevPage}
                  disabled={currentPage === 0}
                  className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm text-white px-6 py-3 rounded-lg border border-white/20 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  <ChevronLeft className="h-5 w-5" />
                  <span>Previous</span>
                </button>

                <div className="flex space-x-2">
                  {pages.map((_, index) => (
                    <div
                      key={index}
                      className={`w-3 h-3 rounded-full transition-all duration-200 ${
                        index === currentPage ? 'bg-orange-500' : 'bg-white/30'
                      }`}
                    />
                  ))}
                </div>

                <button
                  onClick={nextPage}
                  disabled={currentPage === pages.length - 1}
                  className="flex items-center space-x-2 bg-white/10 backdrop-blur-sm text-white px-6 py-3 rounded-lg border border-white/20 hover:bg-white/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                >
                  <span>Next</span>
                  <ChevronRight className="h-5 w-5" />
                </button>
              </div>

              {/* Instructions */}
              <div className="text-center">
                <p className="text-white/60 text-sm">
                  Use arrow keys or click to navigate • {currentPage + 1} of {pages.length}
                </p>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default FantasyBasketballWrapped;
'use client';

import { useState, useRef, useEffect } from 'react';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage.trim(),
      sender: 'user',
      timestamp: new Date().toLocaleTimeString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.text,
          max_length: 150,
          temperature: 0.7,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get response from chatbot. Please try again.');

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString(),
        isError: true,
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestedQuestions = [
    "What are the symptoms of diabetes?",
    "How can I improve my sleep quality?",
    "What should I do for a headache?",
    "Explain hypertension treatment"
  ];

  const handleSuggestionClick = (question) => {
    setInputMessage(question);
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Modern Header with Gradient */}
      <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 shadow-lg">
        <div className="px-6 py-6">
          <div className="flex items-center space-x-4">
            <div className="bg-white/20 backdrop-blur-sm p-3 rounded-2xl shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Medical AI Assistant</h1>
              <p className="text-blue-100 text-sm flex items-center space-x-1">
                <span className="inline-block w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                <span>Powered by Qwen 2.5 • Always here to help</span>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container with Enhanced Design */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center max-w-2xl px-6">
              {/* Animated Icon */}
              <div className="mb-6 relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full blur-2xl opacity-30 animate-pulse"></div>
                <div className="relative bg-gradient-to-br from-blue-500 to-purple-600 w-24 h-24 mx-auto rounded-3xl flex items-center justify-center transform hover:scale-110 transition-transform duration-300 shadow-2xl">
                  <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
              </div>
              
              <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
                Welcome to Your Medical AI Assistant
              </h2>
              <p className="text-gray-600 mb-8 text-lg">
                Ask me anything about medical conditions, symptoms, or health advice. I'm here to help! 🩺
              </p>

              {/* Suggested Questions */}
              <div className="space-y-3">
                <p className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Try asking:</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {suggestedQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => handleSuggestionClick(question)}
                      className="group bg-white hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 border-2 border-gray-200 hover:border-blue-300 rounded-xl p-4 text-left transition-all duration-300 shadow-sm hover:shadow-lg transform hover:-translate-y-1"
                    >
                      <div className="flex items-start space-x-3">
                        <svg className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span className="text-sm text-gray-700 group-hover:text-gray-900 font-medium">{question}</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
          >
            <div className={`flex items-start space-x-3 max-w-2xl ${message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              {/* Avatar */}
              <div className={`shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
                message.sender === 'user'
                  ? 'bg-gradient-to-br from-blue-500 to-purple-600'
                  : 'bg-gradient-to-br from-indigo-500 to-blue-600'
              }`}>
                {message.sender === 'user' ? (
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                ) : (
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`px-5 py-3 rounded-2xl shadow-md transition-all duration-300 hover:shadow-lg ${
                  message.sender === 'user'
                    ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-tr-sm'
                    : message.isError
                    ? 'bg-red-50 text-red-800 border-2 border-red-200 rounded-tl-sm'
                    : 'bg-white text-gray-800 border border-gray-200 rounded-tl-sm'
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
                <p className={`text-xs mt-2 flex items-center space-x-1 ${
                  message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{message.timestamp}</span>
                </p>
              </div>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start animate-fadeIn">
            <div className="flex items-start space-x-3 max-w-2xl">
              {/* Bot Avatar */}
              <div className="shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-gradient-to-br from-indigo-500 to-blue-600 shadow-lg">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              
              {/* Typing Indicator */}
              <div className="bg-white border border-gray-200 px-5 py-4 rounded-2xl rounded-tl-sm shadow-md">
                <div className="flex items-center space-x-3">
                  <div className="flex space-x-1.5">
                    <div className="w-2.5 h-2.5 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full animate-bounce"></div>
                    <div className="w-2.5 h-2.5 bg-gradient-to-r from-indigo-400 to-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2.5 h-2.5 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-600 font-medium">AI is thinking...</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="mx-4 bg-red-50 border-l-4 border-red-500 rounded-lg p-4 shadow-md animate-fadeIn">
            <div className="flex items-start space-x-3">
              <svg className="w-5 h-5 text-red-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-800 text-sm font-medium">{error}</p>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Enhanced Input Form */}
      <div className="bg-white/80 backdrop-blur-lg border-t border-gray-200 px-6 py-5 shadow-2xl">
        <form onSubmit={sendMessage} className="max-w-4xl mx-auto">
          <div className="flex items-end space-x-3">
            {/* Input Field */}
            <div className="flex-1 relative">
              <textarea
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage(e);
                  }
                }}
                placeholder="Ask me anything about health or medical conditions..."
                rows="1"
                className="w-full px-5 py-4 pr-12 border-2 border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none shadow-sm transition-all duration-200 hover:border-gray-400 text-gray-900 bg-white placeholder:text-gray-400"
                disabled={isLoading}
                style={{ minHeight: '56px', maxHeight: '120px' }}
              />
              <div className="absolute right-4 bottom-4 text-xs text-gray-400">
                Press Enter to send
              </div>
            </div>

            {/* Send Button */}
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim()}
              className="shrink-0 px-6 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 disabled:transform-none font-semibold flex items-center space-x-2"
            >
              {isLoading ? (
                <>
                  <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Sending...</span>
                </>
              ) : (
                <>
                  <span>Send</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </>
              )}
            </button>
          </div>
          
          {/* Helper Text */}
          <p className="text-xs text-gray-500 mt-3 text-center">
            💡 This AI provides general medical information. Always consult a healthcare professional for medical advice.
          </p>
        </form>
      </div>
    </div>
  );
}
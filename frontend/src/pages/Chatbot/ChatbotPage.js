import React from 'react';
import Layout from '../../components/common/Layout';

const ChatbotPage = () => {
  return (
    <Layout>
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-6 text-center">Crime Prediction Chatbot</h1>
          <p className="text-secondary mb-12 text-center max-w-2xl mx-auto">
            This feature will be implemented in future milestones. For now, this is a placeholder page.
          </p>
          
          <div className="bg-gray-900 rounded-lg p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold">Chat</h2>
              <div className="bg-primary text-white px-4 py-2 rounded-full text-sm">Coming Soon</div>
            </div>
            
            <div className="h-96 border border-gray-800 rounded-lg flex items-center justify-center">
              <p className="text-secondary">Chatbot interface will be available in future updates</p>
            </div>
            
            <div className="mt-6 flex items-center">
              <input 
                type="text" 
                placeholder="Ask about crime safety in any area..." 
                className="flex-grow bg-black border border-gray-800 rounded-l-lg py-3 px-4 focus:outline-none focus:border-primary"
                disabled
              />
              <button className="bg-primary text-white py-3 px-6 rounded-r-lg opacity-50 cursor-not-allowed">
                Send
              </button>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default ChatbotPage; 
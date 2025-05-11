import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-black border-t border-[#1c1c1c] py-16 relative overflow-hidden">
      {/* Texture overlay */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjMDAwIj48L3JlY3Q+CjxwYXRoIGQ9Ik0wIDVMNSAwWk02IDRMNCA2Wk0tMSAxTDEgLTFaIiBzdHJva2U9IiMyMjIiIHN0cm9rZS13aWR0aD0iMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-10"></div>
      
      <div className="container mx-auto px-4 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10 md:gap-8 text-center md:text-left">
          {/* Column 1 - Project Description */}
          <div className="col-span-1 space-y-6 flex flex-col items-center md:items-start">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold tracking-wider text-white">CrimeFinder</span>
            </Link>
            <p className="text-[#e2e2e2] text-sm max-w-xs">
              A data visualization project for crime statistics analysis. Developed as part of a college assignment in data science and web development.
            </p>
          </div>
          
          {/* Column 2 - About Project */}
          <div className="space-y-6 flex flex-col items-center md:items-start">
            <h3 className="text-white font-bold text-lg">About Project</h3>
            <ul className="space-y-4 text-[#e2e2e2] text-center md:text-left">
              <li><Link to="/methodology" className="hover:text-[#bc2424] transition-colors">Methodology</Link></li>
              <li><Link to="/data-sources" className="hover:text-[#bc2424] transition-colors">Data Sources</Link></li>
              <li><Link to="/tech-stack" className="hover:text-[#bc2424] transition-colors">Tech Stack</Link></li>
              <li><Link to="/documentation" className="hover:text-[#bc2424] transition-colors">Documentation</Link></li>
            </ul>
          </div>
          
          {/* Column 3 - Contact */}
          <div className="space-y-6 flex flex-col items-center md:items-start">
            <h3 className="text-white font-bold text-lg">Contact</h3>
            <ul className="space-y-4 text-[#e2e2e2] text-center md:text-left">
              <li><a href="mailto:student@university.edu" className="hover:text-[#bc2424] transition-colors">student@university.edu</a></li>
              <li><Link to="/about-team" className="hover:text-[#bc2424] transition-colors">About the Team</Link></li>
              <li><a href="https://github.com/username/crimefinder" target="_blank" rel="noopener noreferrer" className="hover:text-[#bc2424] transition-colors">GitHub Repository</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-[#1c1c1c] mt-16 pt-8 flex flex-col md:flex-row justify-center md:justify-between items-center">
          <p className="text-[#e2e2e2] text-center md:text-left">© {new Date().getFullYear()} CrimeFinder. Created for educational purposes only.</p>
          <div className="flex space-x-6 mt-6 md:mt-0 justify-center">
            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-[#e2e2e2] hover:text-[#bc2424] transition-colors">
              <span className="sr-only">GitHub</span>
              <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 
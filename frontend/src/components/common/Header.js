import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="absolute top-0 left-0 right-0 z-50">
      <div className="container mx-auto px-6 py-5 flex justify-between items-center">
        <div className="flex items-center">
          <Link to="/" className="flex items-center">
            <span className="text-xl font-bold tracking-wider text-white">COINFLIP</span>
          </Link>
        </div>
        
        <nav className="hidden md:flex items-center space-x-8">
          <Link to="/buy-sell" className="text-white hover:text-[#B982FF] transition-colors text-sm font-medium">Buy / Sell</Link>
          <Link to="/grow" className="text-white hover:text-[#B982FF] transition-colors text-sm font-medium">Grow</Link>
          <Link to="/markets" className="text-white hover:text-[#B982FF] transition-colors text-sm font-medium">Markets</Link>
          <Link to="/business" className="text-white hover:text-[#B982FF] transition-colors text-sm font-medium">Business</Link>
          <Link to="/support" className="text-white hover:text-[#B982FF] transition-colors text-sm font-medium">Support</Link>
        </nav>
        
        <div className="hidden md:flex items-center space-x-3">
          <Link to="/login" className="text-white hover:text-[#B982FF] transition-colors px-4 py-2 rounded-full border border-transparent hover:border-white/20">
            Sign in
          </Link>
          <Link to="/signup" className="bg-gradient-to-r from-[#6366F1] to-[#8B5CF6] text-white font-medium py-2 px-6 rounded-full hover:opacity-90 transition-opacity">
            Sign up
          </Link>
        </div>

        {/* Mobile menu button */}
        <button 
          type="button" 
          className="md:hidden rounded-md p-2 text-white"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#0C0E16]/90 backdrop-blur-sm py-4">
          <div className="container mx-auto px-4 space-y-2">
            <Link to="/buy-sell" className="block py-2 text-white hover:text-[#B982FF]">Buy / Sell</Link>
            <Link to="/grow" className="block py-2 text-white hover:text-[#B982FF]">Grow</Link>
            <Link to="/markets" className="block py-2 text-white hover:text-[#B982FF]">Markets</Link>
            <Link to="/business" className="block py-2 text-white hover:text-[#B982FF]">Business</Link>
            <Link to="/support" className="block py-2 text-white hover:text-[#B982FF]">Support</Link>
            <div className="pt-4 flex flex-col space-y-3">
              <Link to="/login" className="block text-white hover:text-[#B982FF] py-2">
                Sign in
              </Link>
              <Link to="/signup" className="block bg-gradient-to-r from-[#6366F1] to-[#8B5CF6] text-white font-medium py-2 px-4 rounded-full text-center">
                Sign up
              </Link>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header; 
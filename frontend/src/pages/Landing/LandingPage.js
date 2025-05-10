import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';

const FeatureCard = ({ title, description, icon, buttonText = "Get Started" }) => {
  return (
    <div className="bg-[#1A1B23] rounded-3xl p-8 flex flex-col items-center transition-transform hover:scale-105">
      <div className="w-16 h-16 rounded-full flex items-center justify-center bg-black bg-opacity-30 mb-6">
        {icon}
      </div>
      <h3 className="text-white text-3xl font-bold mb-4 text-center">{title}</h3>
      <p className="text-[#898CA9] text-center mb-6">{description}</p>
      <button className="mt-auto flex items-center text-[#B982FF] hover:text-white group">
        <span className="mr-2">{buttonText}</span>
        <svg className="w-4 h-4 stroke-[#B982FF] group-hover:stroke-white" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </button>
    </div>
  );
};

const GradientButton = ({ children, className = "" }) => {
  return (
    <button 
      className={`bg-gradient-to-r from-[#6366F1] to-[#8B5CF6] text-white font-medium py-3 px-8 rounded-full hover:opacity-90 transition-opacity ${className}`}
    >
      {children}
    </button>
  );
};

// Colorful planet/sphere element
const Planet = ({ color, size, className }) => {
  return (
    <div 
      className={`rounded-full ${className}`} 
      style={{ 
        width: size, 
        height: size, 
        background: color,
        boxShadow: `0 0 60px ${color}`
      }}
    ></div>
  );
};

// Star element
const Star = ({ size, className }) => {
  return (
    <div className={`${className}`}>
      <svg className={`w-${size} h-${size} text-white`} viewBox="0 0 24 24">
        <path fill="currentColor" d="M12,1L9,9L1,12L9,15L12,23L15,15L23,12L15,9L12,1Z"/>
      </svg>
    </div>
  );
};

const LandingPage = () => {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="min-h-screen relative overflow-hidden flex flex-col justify-center items-center pt-24 pb-16">
        {/* Background gradient */}
        <div className="absolute inset-0 z-0 bg-gradient-to-br from-[#051937] via-[#0E4257] to-[#052E34]">
          {/* Background circular pattern */}
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0gMCAxMDAgQSAxMDAgMTAwIDAgMCAxIDEwMCAwIEwgMTAwIDEwMCBaIiBmaWxsPSJub25lIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4xKSIgc3Ryb2tlLXdpZHRoPSIwLjUiPjwvcGF0aD48L3N2Zz4=')] opacity-20"></div>
          
          {/* Decorative elements */}
          <Planet 
            color="linear-gradient(180deg, #FF8D69 0%, #D62C2C 100%)" 
            size="70px" 
            className="absolute left-16 bottom-1/4 animate-pulse-slow"
          />
          
          <Planet 
            color="linear-gradient(180deg, #9661FF 0%, #6F00FF 100%)" 
            size="100px" 
            className="absolute right-32 bottom-20 animate-pulse-slow"
          />
          
          <Planet 
            color="linear-gradient(180deg, #61B2FF 0%, #0062FF 100%)" 
            size="50px" 
            className="absolute right-1/4 top-32 animate-pulse-slow"
          />
          
          {/* Star elements */}
          <Star size="8" className="absolute top-1/4 left-1/4 rotate-12" />
          <Star size="5" className="absolute top-28 right-1/3 rotate-45" />
          <Star size="6" className="absolute bottom-1/3 right-1/5 -rotate-12" />
        </div>
        
        <div className="container mx-auto px-4 relative z-10 text-center">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-7xl font-black leading-tight mb-6">
              We make crime finding clear and simple
            </h1>
            <p className="text-[#E0E0E0] text-xl md:text-2xl mb-12 max-w-2xl mx-auto">
              Find the crime for a place, quick and easy.
            </p>
            <GradientButton>Get Started</GradientButton>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-black relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          {/* Background circle patterns from Figma */}
          <div className="absolute top-0 left-0 w-[500px] h-[500px] rounded-full border border-[#484848] opacity-30"></div>
          <div className="absolute bottom-0 right-0 w-[600px] h-[600px] rounded-full border border-[#484848] opacity-20"></div>
        </div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-black mb-6">A crime finding platform that saves the future you</h2>
            <p className="text-[#898CA9] text-xl mx-auto max-w-3xl">
              Our team put a lot of effort to make a platform to make sure that you stay safe outdoors
            </p>
            <GradientButton className="mt-6">Get Started</GradientButton>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
            <FeatureCard 
              title="Specify Location" 
              description="Enter any location by address or coordinates and our system will analyze the area."
              icon={
                <img src="/assets/location-icon.svg" alt="Location" className="w-8 h-8" />
              }
            />
            
            <FeatureCard 
              title="Choose Time" 
              description="Select a specific date and time to get crime risk assessments for that moment."
              icon={
                <img src="/assets/time-icon.svg" alt="Time" className="w-8 h-8" />
              }
              buttonText="Find an ATM"
            />
            
            <FeatureCard 
              title="Get Risk Rate" 
              description="Receive detailed crime risk analysis and safety recommendations instantly."
              icon={
                <img src="/assets/risk-icon.svg" alt="Risk" className="w-8 h-8" />
              }
              buttonText="Download the App"
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 z-0">
          {/* Background gradients from Figma */}
          <div className="absolute top-0 right-0 w-[400px] h-[400px] rounded-full bg-gradient-to-br from-[#00C2FF]/5 to-[#FF29C3]/20 blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-[400px] h-[400px] rounded-full bg-gradient-to-br from-[#184BFF]/5 to-[#174AFF]/20 blur-3xl"></div>
        </div>
        
        <div className="container mx-auto px-4 relative z-10 text-center">
          <h2 className="text-5xl font-black mb-8">Take your first step<br />into safe, secure future</h2>
          <GradientButton>Get Started</GradientButton>
        </div>
      </section>
    </Layout>
  );
};

export default LandingPage; 
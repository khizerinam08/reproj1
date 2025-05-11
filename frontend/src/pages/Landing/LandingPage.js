import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../../components/common/Layout';
import TextReveal from '../../components/animation/TextReveal';
import FadeIn from '../../components/animation/FadeIn';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger);

const FeatureCard = ({ title, description, icon, buttonText = "Learn More" }) => {
  return (
    <div className="bg-[#141414] rounded-3xl p-8 flex flex-col items-center transition-transform hover:scale-105">
      <div className="w-16 h-16 rounded-full flex items-center justify-center bg-black bg-opacity-30 mb-6">
        {icon}
      </div>
      <h3 className="text-white text-3xl font-bold mb-4 text-center">{title}</h3>
      <p className="text-[#e2e2e2] text-center mb-6">{description}</p>
      <button className="mt-auto flex items-center text-[#bc2424] hover:text-white group">
        <span className="mr-2">{buttonText}</span>
        <svg className="w-4 h-4 stroke-[#bc2424] group-hover:stroke-white" fill="none" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </button>
    </div>
  );
};

const PrimaryButton = ({ children, className = "", onClick, to }) => {
  // If 'to' prop is provided, render a Link instead of a button
  if (to) {
    return (
      <Link 
        to={to}
        className={`bg-[#bc2424] text-white font-medium py-3 px-8 rounded-full hover:opacity-90 transition-opacity ${className}`}
      >
        {children}
      </Link>
    );
  }
  
  // Regular button
  return (
    <button 
      className={`bg-[#bc2424] text-white font-medium py-3 px-8 rounded-full hover:opacity-90 transition-opacity ${className}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

// Colorful planet/sphere element with more dynamic animation
const Planet = ({ color, size, className, speed = 1 }) => {
  return (
    <div 
      className={`rounded-full animate-float ${className}`} 
      data-speed={speed}
      style={{ 
        width: size, 
        height: size, 
        background: color,
        boxShadow: `0 0 60px ${color}`,
        animation: `float ${Math.random() * 10 + 15}s ease-in-out infinite, 
                  pulse ${Math.random() * 5 + 3}s ease-in-out infinite`
      }}
    ></div>
  );
};

// Star element with rotation
const Star = ({ size, className, speed = 1.2 }) => {
  return (
    <div 
      className={`${className} animate-twinkle`} 
      data-speed={speed}
      style={{
        animation: `twinkle ${Math.random() * 5 + 3}s ease-in-out infinite, 
                  rotate ${Math.random() * 20 + 20}s linear infinite`
      }}
    >
      <svg className={`w-${size} h-${size} text-white`} viewBox="0 0 24 24">
        <path fill="currentColor" d="M12,1L9,9L1,12L9,15L12,23L15,15L23,12L15,9L12,1Z"/>
      </svg>
    </div>
  );
};

// Location icon component
const LocationIcon = () => (
  <svg className="w-8 h-8 text-[#bc2424]" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2ZM12 11.5C10.62 11.5 9.5 10.38 9.5 9C9.5 7.62 10.62 6.5 12 6.5C13.38 6.5 14.5 7.62 14.5 9C14.5 10.38 13.38 11.5 12 11.5Z" 
      fill="currentColor"/>
  </svg>
);

// Time icon component
const TimeIcon = () => (
  <svg className="w-8 h-8 text-[#bc2424]" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.5 2 2 6.5 2 12C2 17.5 6.5 22 12 22C17.5 22 22 17.5 22 12C22 6.5 17.5 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20ZM12.5 7H11V13L16.2 16.2L17 14.9L12.5 12.2V7Z" 
      fill="currentColor"/>
  </svg>
);

// Risk icon component
const RiskIcon = () => (
  <svg className="w-8 h-8 text-[#bc2424]" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L1 21H23L12 2ZM12 6L19.53 19H4.47L12 6ZM11 10V14H13V10H11ZM11 16V18H13V16H11Z" 
      fill="currentColor"/>
  </svg>
);

const LandingPage = () => {
  // Create a reference to the canvas element
  const canvasRef = useRef(null);
  const heroRef = useRef(null);
  const featuresRef = useRef(null);
  const ctaRef = useRef(null);

  // Effect to create the noise texture
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    
    // Set canvas size based on device pixel ratio
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    
    // Function to draw noise
    function drawNoise() {
      // Create noise pattern
      const imageData = ctx.createImageData(canvas.width, canvas.height);
      const data = imageData.data;
      
      for (let i = 0; i < data.length; i += 4) {
        // Randomize noise with very low opacity
        const randomValue = Math.floor(Math.random() * 255);
        data[i] = randomValue;      // red
        data[i + 1] = randomValue;  // green
        data[i + 2] = randomValue;  // blue
        data[i + 3] = Math.random() * 10; // alpha (very low)
      }
      
      ctx.putImageData(imageData, 0, 0);
    }
    
    // Initial draw and interval for animation
    drawNoise();
    const noiseInterval = setInterval(drawNoise, 100);
    
    // Clean up interval on unmount
    return () => clearInterval(noiseInterval);
  }, []);

  // Initialize parallax effects using the data-speed attributes
  useEffect(() => {
    // Wait for any layout shifts to settle
    const initParallax = setTimeout(() => {
      // Select all elements with data-speed attribute
      const parallaxElements = document.querySelectorAll("[data-speed]");
      
      parallaxElements.forEach(element => {
        const speed = parseFloat(element.getAttribute("data-speed") || 1);
        
        // Create the parallax effect
        gsap.to(element, {
          y: () => {
            const scrollDistance = window.innerHeight * 0.5; // Half the viewport height
            return scrollDistance * speed * -0.1; // Negative to move against scroll
          },
          ease: "none",
          scrollTrigger: {
            trigger: element.closest('section') || element,
            start: "top bottom",
            end: "bottom top",
            scrub: 0.5, // Smooth scrubbing effect
          }
        });
      });
    }, 500);
    
    return () => clearTimeout(initParallax);
  }, []);

  return (
    <Layout>
      {/* Hero Section */}
      <section 
        ref={heroRef}
        className="min-h-screen relative overflow-hidden flex flex-col justify-center items-center pt-24 pb-16">
        {/* Canvas for noise texture */}
        <canvas 
          ref={canvasRef}
          className="absolute inset-0 z-0 opacity-5"
          style={{ width: '100%', height: '100%' }}
        />
        
        {/* Background with circular orbits and gradient */}
        <div className="absolute inset-0 z-0 bg-gradient-radial from-black via-[#120909] to-black">
          {/* Rough texture overlay */}
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjMDAwIj48L3JlY3Q+CjxwYXRoIGQ9Ik0wIDVMNSAwWk02IDRMNCA2Wk0tMSAxTDEgLTFaIiBzdHJva2U9IiMyMjIiIHN0cm9rZS13aWR0aD0iMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-10"></div>
          
          {/* Circular orbit lines */}
          <div className="absolute inset-0 overflow-hidden animate-slow-spin">
            <div className="absolute w-[200%] h-[200%] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
              <div className="absolute w-full h-full border border-[#222222] rounded-full"></div>
              <div className="absolute w-[80%] h-[80%] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border border-[#222222] rounded-full"></div>
              <div className="absolute w-[60%] h-[60%] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border border-[#222222] rounded-full"></div>
              <div className="absolute w-[40%] h-[40%] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 border border-[#222222] rounded-full"></div>
            </div>
          </div>
          
          {/* 3D Icons - Water-like floating animation with enhanced glow */}
          <div style={{ 
            position: 'absolute', 
            left: '8%', 
            top: '65%',
            animation: 'gentleFloat 8s ease-in-out infinite',
            zIndex: 1
          }} className="icon-container">
            <div className="relative">
              <div className="absolute inset-[-5px] bg-white/10 blur-md rounded-full opacity-80"></div>
              <img 
                src="/assets/siren.png" 
                alt="Police Siren" 
                className="relative filter drop-shadow-2xl responsive-icon" 
                style={{ transform: 'rotate(-3deg)' }}
              />
            </div>
          </div>
          
          <div style={{ 
            position: 'absolute', 
            right: '5%', 
            top: '20%',
            animation: 'gentleFloat 9s ease-in-out infinite 1s',
            zIndex: 1
          }} className="icon-container">
            <div className="relative">
              <div className="absolute inset-[-5px] bg-white/10 blur-md rounded-full opacity-80"></div>
              <img 
                src="/assets/location.png" 
                alt="Location Marker" 
                className="relative filter drop-shadow-2xl responsive-icon" 
                style={{ transform: 'rotate(3deg)' }}
              />
            </div>
          </div>
          
          {/* Decorative elements */}
          <Planet 
            color="#bc2424" 
            size="70px" 
            className="absolute left-20 bottom-2/4"
          />
          
          <Planet 
            color="#bc2424" 
            size="100px" 
            className="absolute right-32 bottom-20 opacity-80"
          />
          
          <Planet 
            color="#bc2424" 
            size="50px" 
            className="absolute right-1/4 top-32 opacity-60"
          />
          
          {/* Star elements */}
          <Star size="8" className="absolute top-1/4 left-1/4" />
          <Star size="5" className="absolute top-28 right-1/3" />
          <Star size="6" className="absolute bottom-1/3 right-1/5" />
          <Star size="4" className="absolute top-1/6 left-1/3" />
          <Star size="7" className="absolute bottom-1/4 left-1/2" />
        </div>
        
        <div className="container mx-auto px-4 relative z-10 text-center">
          <div className="max-w-4xl mx-auto">
            <TextReveal>
              <h1 className="text-5xl md:text-7xl font-black leading-tight mb-6">
                Crime data analysis made simple
              </h1>
            </TextReveal>
            
            <TextReveal delay={0.2}>
              <p className="text-[#e2e2e2] text-xl md:text-2xl mb-12 max-w-2xl mx-auto">
                A college project demonstrating crime data visualization and predictive analysis
              </p>
            </TextReveal>
            
            <FadeIn delay={0.4} fromY={20}>
              <div className="flex flex-wrap gap-4 justify-center">
                <PrimaryButton to="/signup">Create Account</PrimaryButton>
                <PrimaryButton to="/login" className="bg-transparent border border-[#bc2424] hover:bg-[#bc2424]/20">
                  Sign In
                </PrimaryButton>
              </div>
            </FadeIn>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section 
        ref={featuresRef}
        className="py-20 bg-black relative overflow-hidden">
        <div className="absolute inset-0 z-0 bg-gradient-to-b from-black via-[#0a0000] to-black">
          {/* Background texture overlay */}
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjMDAwIj48L3JlY3Q+CjxwYXRoIGQ9Ik0wIDVMNSAwWk02IDRMNCA2Wk0tMSAxTDEgLTFaIiBzdHJva2U9IiMyMjIiIHN0cm9rZS13aWR0aD0iMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-10"></div>
          
          {/* Background circle patterns */}
          <div className="absolute top-0 left-0 w-[500px] h-[500px] rounded-full border border-[#222222] opacity-30 animate-slow-spin"></div>
          <div className="absolute bottom-0 right-0 w-[600px] h-[600px] rounded-full border border-[#222222] opacity-20 animate-reverse-spin"></div>
        </div>
        
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center mb-16">
            <TextReveal>
              <h2 className="text-4xl md:text-5xl font-black mb-6">Data-driven crime analysis for academic research</h2>
            </TextReveal>
            
            <TextReveal delay={0.2}>
              <p className="text-[#e2e2e2] text-xl mx-auto max-w-3xl">
                This project demonstrates the application of data science techniques to crime statistics for educational purposes
              </p>
            </TextReveal>
            
            <FadeIn delay={0.3}>
              <PrimaryButton to="/signup" className="mt-6">Get Started</PrimaryButton>
            </FadeIn>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
            <FadeIn delay={0.1} fromY={50} threshold="10% bottom">
              <FeatureCard 
                title="Specify Location" 
                description="Select geographic areas of interest to visualize crime data patterns and statistical trends."
                icon={<LocationIcon />}
              />
            </FadeIn>
            
            <FadeIn delay={0.2} fromY={50} threshold="10% bottom">
              <FeatureCard 
                title="Choose Time" 
                description="Analyze temporal patterns in crime data, including time of day, day of week, and seasonal variations."
                icon={<TimeIcon />}
                buttonText="See Analysis"
              />
            </FadeIn>
            
            <FadeIn delay={0.3} fromY={50} threshold="10% bottom">
              <FeatureCard 
                title="Get Risk Rate" 
                description="Explore our machine learning model that calculates crime risk factors based on historical data."
                icon={<RiskIcon />}
                buttonText="View Methodology"
              />
            </FadeIn>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section 
        ref={ctaRef}
        className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 z-0 bg-gradient-to-b from-black from-40% via-black via-60% to-[#bc2424] to-100%">
          {/* Background texture overlay */}
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjMDAwIj48L3JlY3Q+CjxwYXRoIGQ9Ik0wIDVMNSAwWk02IDRMNCA2Wk0tMSAxTDEgLTFaIiBzdHJva2U9IiMyMjIiIHN0cm9rZS13aWR0aD0iMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-10"></div>
          
          {/* Moved the blur effects higher */}
          <div className="absolute top-1/4 right-0 w-[400px] h-[400px] rounded-full bg-[#bc2424]/20 blur-3xl animate-pulse-slow"></div>
          <div className="absolute top-1/2 left-0 w-[500px] h-[400px] rounded-full bg-[#bc2424]/30 blur-3xl animate-pulse-slow"></div>
          
          {/* Floating elements */}
          <Star size="6" className="absolute top-20 left-1/5" />
          <Star size="4" className="absolute bottom-40 right-40" />
          <Planet 
            color="#bc2424" 
            size="40px" 
            className="absolute left-1/4 top-1/3 opacity-40"
          />
        </div>
        
        <div className="container mx-auto px-4 relative z-10 text-center">
          <TextReveal>
            <h2 className="text-5xl font-black mb-8">Explore our research<br />on crime data analysis</h2>
          </TextReveal>
          
          <FadeIn delay={0.3} fromY={30}>
            <div className="flex flex-wrap gap-4 justify-center">
              <PrimaryButton to="/signup">Get Started</PrimaryButton>
              <PrimaryButton to="/login" className="bg-transparent border border-[#bc2424] hover:bg-[#bc2424]/20">
                Sign In
              </PrimaryButton>
            </div>
          </FadeIn>
        </div>
      </section>

      {/* Add custom keyframes for gentle floating */}
      <style>
        {`
        @keyframes gentleFloat {
          0%, 100% { 
            transform: translateY(0px) rotate(-2deg); 
          }
          25% { 
            transform: translateY(-8px) rotate(0deg); 
          }
          50% { 
            transform: translateY(0px) rotate(2deg); 
          }
          75% { 
            transform: translateY(8px) rotate(0deg); 
          }
        }
        
        .responsive-icon {
          width: 120px;
        }
        
        @media (max-width: 1200px) {
          .responsive-icon {
            width: 100px;
          }
        }
        
        @media (max-width: 768px) {
          .responsive-icon {
            width: 80px;
          }
          .icon-container {
            top: 10% !important;
          }
        }
        
        @media (max-width: 640px) {
          .icon-container:first-of-type {
            left: 2% !important;
            top: 60% !important;
          }
          .icon-container:last-of-type {
            right: 2% !important;
          }
        }
        
        @media (max-width: 480px) {
          .responsive-icon {
            width: 60px;
          }
          .icon-container:first-of-type {
            top: 50% !important;
          }
          .icon-container:last-of-type {
            top: 5% !important;
          }
        }
        `}
      </style>
    </Layout>
  );
};

export default LandingPage; 
import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register plugins
gsap.registerPlugin(ScrollTrigger);

// Text animation component that reveals text as it enters the viewport
const TextReveal = ({ children, stagger = 0.05, duration = 1, ease = "power3.out", className = "" }) => {
  const textRef = useRef(null);
  const containerRef = useRef(null);
  
  useEffect(() => {
    if (!textRef.current) return;

    // Store a reference to the current element
    const textElement = textRef.current;
    
    // Split text into lines or paragraphs if needed
    const isMultipleElements = textElement.children.length > 0;
    let targets = [];

    if (isMultipleElements) {
      // Target each child element (like paragraphs or headings)
      targets = [...textElement.children];
    } else {
      // Target single element
      targets = [textElement];
    }

    // Create animation for each target
    targets.forEach((target) => {
      // Initial state - invisible and moved down slightly
      gsap.set(target, { 
        opacity: 0,
        y: 30
      });
      
      // Create the reveal animation triggered by scroll
      gsap.to(target, {
        opacity: 1,
        y: 0,
        duration: duration,
        ease: ease,
        scrollTrigger: {
          trigger: target,
          start: "top 85%", // Start when the top of the element is 85% from the top of the viewport
          end: "bottom 60%",
          toggleActions: "play none none none", // play, reverse, restart, reset
          // markers: true, // Uncomment for debugging
        }
      });
    });
    
    // Clean up
    return () => {
      const triggers = ScrollTrigger.getAll();
      triggers.forEach(trigger => {
        // Check if the trigger is related to our elements
        if (targets.includes(trigger.vars.trigger)) {
          trigger.kill();
        }
      });
    };
  }, [duration, ease, stagger]);
  
  return (
    <div ref={containerRef} className={`overflow-hidden ${className}`}>
      <div ref={textRef} className="will-change-transform">
        {children}
      </div>
    </div>
  );
};

export default TextReveal; 
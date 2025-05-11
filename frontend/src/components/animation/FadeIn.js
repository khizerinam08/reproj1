import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

// Register plugins
gsap.registerPlugin(ScrollTrigger);

// Animation component that fades in and slides up elements as they enter the viewport
const FadeIn = ({ 
  children, 
  delay = 0, 
  duration = 0.8, 
  fromY = 40, 
  ease = "power3.out", 
  threshold = "20% bottom", 
  className = "" 
}) => {
  const elementRef = useRef(null);
  
  useEffect(() => {
    if (!elementRef.current) return;
    
    // Store a reference to the current element
    const element = elementRef.current;
    
    // Initial state - invisible and moved down
    gsap.set(element, { 
      opacity: 0,
      y: fromY
    });
    
    // Create the fade-in animation triggered by scroll
    const animation = gsap.to(element, {
      opacity: 1,
      y: 0,
      duration: duration,
      delay: delay,
      ease: ease,
      scrollTrigger: {
        trigger: element,
        start: threshold,
        toggleActions: "play none none none",
        // markers: true, // Uncomment for debugging
      }
    });
    
    // Clean up
    return () => {
      if (animation) {
        animation.kill();
      }
      const trigger = ScrollTrigger.getAll().find(
        t => t.vars.trigger === element
      );
      if (trigger) {
        trigger.kill();
      }
    };
  }, [delay, duration, fromY, ease, threshold]);
  
  return (
    <div ref={elementRef} className={`will-change-transform ${className}`}>
      {children}
    </div>
  );
};

export default FadeIn; 
"""
Script to examine the crime prediction model file using joblib.
"""
import os
import sys
import numpy as np

# Try different libraries for loading
try:
    import joblib
    print("Using joblib to load model")
    use_joblib = True
except ImportError:
    import pickle
    print("Using pickle to load model")
    use_joblib = False

def load_model(model_path):
    """
    Load the model file and print information about it using joblib.
    """
    print(f"Loading model from: {model_path}")
    try:
        if use_joblib:
            model = joblib.load(model_path)
        else:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        
        print(f"Model type: {type(model)}")
        
        # Check model class or module name
        if hasattr(model, "__module__"):
            print(f"Model module: {model.__module__}")
        
        if hasattr(model, "__class__"):
            print(f"Model class: {model.__class__.__name__}")
        
        # For sklearn models
        if hasattr(model, "predict"):
            print("Model has predict method")
            
            if hasattr(model, "predict_proba"):
                print("Model has predict_proba method")
                
            if hasattr(model, "feature_names_in_"):
                print(f"Feature names: {model.feature_names_in_}")
                
            if hasattr(model, "classes_"):
                print(f"Classes: {model.classes_}")
                
            try:
                # Simple dummy prediction attempt
                dummy_input = np.zeros((1, 6))  # Assuming 6 features
                prediction = model.predict(dummy_input)
                print(f"Sample prediction on zeros: {prediction}")
            except Exception as e:
                print(f"Could not make prediction: {e}")
                
        # For numpy arrays
        elif isinstance(model, np.ndarray):
            print(f"Array shape: {model.shape}")
            print(f"Array dtype: {model.dtype}")
            
            # Print content if small enough
            if model.size < 50 or len(model.shape) == 1:
                print(f"Array contents: {model}")
            else:
                print(f"First few elements: {model.flatten()[:20]}")
                
            if len(model.shape) == 2:
                print(f"Number of rows: {model.shape[0]}")
                print(f"Number of columns: {model.shape[1]}")
                print(f"First row: {model[0]}")
            
        # For dictionaries
        elif isinstance(model, dict):
            print(f"Dictionary with {len(model)} keys")
            print(f"Keys: {list(model.keys())}")
            
        # For lists
        elif isinstance(model, list):
            print(f"List with {len(model)} items")
            if len(model) > 0:
                print(f"First item type: {type(model[0])}")
        
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

if __name__ == "__main__":
    # Get the absolute path to the model file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    model_path = os.path.join(project_dir, "crime_model.pkl")
    
    # Load the model
    model = load_model(model_path)
    
    # Try to load with both pickle and joblib
    if use_joblib:
        print("\n\nRe-trying with pickle:")
        import pickle
        try:
            with open(model_path, 'rb') as f:
                pickle_model = pickle.load(f)
            print(f"Pickle load succeeded. Type: {type(pickle_model)}")
        except Exception as e:
            print(f"Pickle load failed: {e}")
    
    # Check if we missed any data in the file
    print("\n\nChecking for multiple objects in file:")
    try:
        with open(model_path, 'rb') as f:
            try:
                objects = []
                while True:
                    try:
                        obj = pickle.load(f)
                        objects.append((type(obj), obj))
                    except EOFError:
                        break
                print(f"Found {len(objects)} objects in file")
                for i, (obj_type, obj) in enumerate(objects):
                    print(f"Object {i+1}: {obj_type}")
                    if isinstance(obj, np.ndarray):
                        print(f"  Shape: {obj.shape}")
                        if len(obj.shape) == 1 and obj.size < 20:
                            print(f"  Content: {obj}")
            except Exception as e:
                print(f"Error reading multiple objects: {e}")
    except Exception as e:
        print(f"Error opening file: {e}") 
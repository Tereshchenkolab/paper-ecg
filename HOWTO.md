[Project Homepage](README.md) / How To

# How To ...

## ... Change the app icon

### 1. Replace `icon.png` at `/src/main/icons/icon.png`.
### 2. Remove the target directory
    
    ```
    $ rm -rf target/
    ```

### 3. Refresh the `.../icons/` files:

    ```
    $ python src/main/icons/updateIcon.py
    ```

### 4. Rebuild

    ```
    $ fbs freeze
    ```
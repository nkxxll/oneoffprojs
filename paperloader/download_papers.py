#!/usr/bin/env python3
"""Download papers from Unpaywall and CrossRef APIs using DOIs."""

import json
import requests
import time
from pathlib import Path
from urllib.parse import quote
import logging
import hashlib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# File validation settings
MAX_PDF_SIZE = 100 * 1024 * 1024  # 100MB
MIN_PDF_SIZE = 10 * 1024  # 10KB
PDF_MAGIC_BYTES = b"%PDF"

# Create papers directory
PAPERS_DIR = Path("papers")
PAPERS_DIR.mkdir(exist_ok=True)

# Load DOIs
with open("dois.json") as f:
    data = json.load(f)

papers = data["papers"]
logger.info(f"Found {len(papers)} papers to download")

# Track results
results = {
    "downloaded": [],
    "failed": [],
    "skipped": []
}


def sanitize_filename(title: str) -> str:
    """Convert title to safe filename."""
    # Remove/replace problematic characters
    safe = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)
    # Limit length
    return safe[:100].strip()


def validate_pdf(filepath: Path) -> bool:
    """Validate that file is a legitimate PDF."""
    try:
        # Check file exists
        if not filepath.exists():
            logger.error(f"  Validation failed: File does not exist")
            return False
        
        file_size = filepath.stat().st_size
        
        # Check file size
        if file_size < MIN_PDF_SIZE:
            logger.error(f"  Validation failed: File too small ({file_size} bytes, min: {MIN_PDF_SIZE})")
            return False
        
        if file_size > MAX_PDF_SIZE:
            logger.error(f"  Validation failed: File too large ({file_size} bytes, max: {MAX_PDF_SIZE})")
            return False
        
        # Check magic bytes
        with open(filepath, "rb") as f:
            header = f.read(10)
        
        if not header.startswith(PDF_MAGIC_BYTES):
            logger.error(f"  Validation failed: Invalid PDF magic bytes (got {header[:10]})")
            return False
        
        # Calculate SHA256 hash
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        file_hash = sha256_hash.hexdigest()
        logger.debug(f"  File hash (SHA256): {file_hash}")
        
        return True
    except Exception as e:
        logger.error(f"  Validation failed: {e}")
        return False


def download_pdf(url: str, filename: str) -> bool:
    """Download PDF from URL."""
    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        filepath = PAPERS_DIR / filename
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # Validate downloaded file
        if not validate_pdf(filepath):
            filepath.unlink()  # Delete invalid file
            logger.error(f"✗ Downloaded but failed validation: {filename}")
            return False
        
        logger.info(f"✓ Downloaded and validated: {filename}")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to download {filename}: {e}")
        return False


def try_unpaywall(doi: str, title: str) -> bool:
    """Try to get paper from Unpaywall API."""
    try:
        url = f"https://api.unpaywall.org/v2/{quote(doi)}?email=user@example.com"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("is_oa"):
            # Try best OA location first
            if data.get("best_oa_location") and data["best_oa_location"].get("url_for_pdf"):
                pdf_url = data["best_oa_location"]["url_for_pdf"]
                filename = f"{sanitize_filename(title)}.pdf"
                
                if download_pdf(pdf_url, filename):
                    results["downloaded"].append({
                        "title": title,
                        "doi": doi,
                        "source": "unpaywall"
                    })
                    return True
            
            # Try all OA locations
            for location in data.get("oa_locations", []):
                if location.get("url_for_pdf"):
                    pdf_url = location["url_for_pdf"]
                    filename = f"{sanitize_filename(title)}.pdf"
                    
                    if download_pdf(pdf_url, filename):
                        results["downloaded"].append({
                            "title": title,
                            "doi": doi,
                            "source": "unpaywall"
                        })
                        return True
        
        return False
    except Exception as e:
        logger.debug(f"Unpaywall lookup failed for {doi}: {e}")
        return False


def try_crossref(doi: str, title: str) -> bool:
    """Try to get paper metadata from CrossRef and find links."""
    try:
        url = f"https://api.crossref.org/v1/works/{quote(doi)}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json().get("message", {})
        
        # Check for links
        for link in data.get("link", []):
            if link.get("content-type") == "application/pdf":
                pdf_url = link.get("URL")
                if pdf_url:
                    filename = f"{sanitize_filename(title)}.pdf"
                    if download_pdf(pdf_url, filename):
                        results["downloaded"].append({
                            "title": title,
                            "doi": doi,
                            "source": "crossref"
                        })
                        return True
        
        return False
    except Exception as e:
        logger.debug(f"CrossRef lookup failed for {doi}: {e}")
        return False


def try_direct_doi_resolution(doi: str, title: str) -> bool:
    """Try to resolve DOI directly and check if it returns a PDF."""
    try:
        url = f"https://doi.org/{quote(doi)}"
        
        # Headers to request PDF directly
        headers = {
            "Accept": "application/pdf",
            "User-Agent": "Mozilla/5.0 (compatible; PaperDownloader/1.0)"
        }
        
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        # Check if response is a PDF
        content_type = response.headers.get("content-type", "").lower()
        if "pdf" in content_type:
            # Download with GET request
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            filename = f"{sanitize_filename(title)}.pdf"
            filepath = PAPERS_DIR / filename
            
            with open(filepath, "wb") as f:
                f.write(response.content)
            
            logger.info(f"✓ Downloaded: {filename} (direct DOI resolution)")
            results["downloaded"].append({
                "title": title,
                "doi": doi,
                "source": "direct_doi"
            })
            return True
        
        return False
    except Exception as e:
        logger.debug(f"Direct DOI resolution failed for {doi}: {e}")
        return False


def main():
    """Download all papers."""
    for i, paper in enumerate(papers, 1):
        title = paper.get("title", "Unknown")
        doi = paper.get("doi")
        
        logger.info(f"\n[{i}/{len(papers)}] {title}")
        
        # Skip papers without DOI
        if not doi:
            logger.warning("  Skipped: No DOI available")
            results["skipped"].append({"title": title})
            continue
        
        # Check if already downloaded
        safe_title = sanitize_filename(title)
        if (PAPERS_DIR / f"{safe_title}.pdf").exists():
            logger.info("  Skipped: Already downloaded")
            results["skipped"].append({"title": title})
            continue
        
        # Try Unpaywall first
        if try_unpaywall(doi, title):
            time.sleep(0.5)  # Be nice to APIs
            continue
        
        time.sleep(0.5)
        
        # Try CrossRef as fallback
        if try_crossref(doi, title):
            time.sleep(0.5)
            continue
        
        time.sleep(0.5)
        
        # Try direct DOI resolution as last resort
        if try_direct_doi_resolution(doi, title):
            time.sleep(0.5)
            continue
        
        logger.warning("  Failed: Not found in Unpaywall, CrossRef, or direct DOI")
        results["failed"].append({"title": title, "doi": doi})
        time.sleep(0.5)
    
    # Print summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"✓ Downloaded: {len(results['downloaded'])}")
    print(f"✗ Failed: {len(results['failed'])}")
    print(f"⊘ Skipped: {len(results['skipped'])}")
    print(f"Total: {len(results['downloaded']) + len(results['failed']) + len(results['skipped'])}")
    
    # Save results
    with open("download_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info("\nResults saved to download_results.json")


if __name__ == "__main__":
    main()

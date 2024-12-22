# Pyright Type Checking Issues in Visual Script

## Dependency and Import Fixes
- [ ] Install `netifaces` package
  ```bash
  pip install netifaces
  ```
- [ ] Verify import statement for `netifaces`
  ```python
  try:
      import netifaces
  except ImportError:
      netifaces = None  # Graceful fallback
  ```

## Type Annotation and Class Definition Fixes
- [ ] Update `CaptureResult` dataclass to ensure all attributes are properly defined
  ```python
  @dataclass
  class CaptureResult:
      page_name: str
      page_path: str
      status: CaptureStatus = CaptureStatus.PENDING
      screenshot_path: Optional[str] = None
      error_message: Optional[str] = None
      capture_duration: float = 0.0
      attempt_count: int = 0
  ```

## Error Handling and Return Type Fixes
- [ ] Refactor retry mechanism in screenshot capture methods
  ```python
  def _retry_screenshot_capture(
      self, 
      page_path: str, 
      max_attempts: int = 3
  ) -> CaptureResult:
      for attempt in range(max_attempts):
          try:
              result = await self.capture_screenshot_from_mkdocs_build(page_path)
              result.attempt_count = attempt + 1
              return result
          except Exception as e:
              if attempt == max_attempts - 1:
                  return CaptureResult(
                      page_path=page_path,
                      page_name=page_path,
                      status=CaptureStatus.FAILED,
                      error_message=str(e)
                  )
  ```

## Parameter Type Fixes
- [ ] Update method signatures to handle `None` for optional parameters
  ```python
  def capture_site_screenshots(
      self, 
      site_directory: str = 'site/', 
      exclude_dirs: Optional[List[str]] = []  # Default to empty list instead of None
  ) -> List[CaptureResult]:
      # Implementation remains the same
  ```

## General Recommendations
- [ ] Use type hints consistently
- [ ] Implement proper error handling
- [ ] Add logging for debugging
- [ ] Consider using `typing.Optional` for nullable fields

## Next Steps
- [ ] Run Pyright after implementing these changes
- [ ] Perform manual testing to ensure functionality
- [ ] Update documentation to reflect type changes
